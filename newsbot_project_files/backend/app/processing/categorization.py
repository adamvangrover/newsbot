from typing import List, Optional, Dict
from transformers import pipeline
import re
import torch

from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

DEFAULT_ZERO_SHOT_MODEL = "facebook/bart-large-mnli"
zero_shot_classifier = None

DEFAULT_CATEGORIES_KEYWORDS = {
    'Financial Performance': ['earnings', 'profit', 'revenue', 'loss', 'growth', 'dividend', 'stock price', 'market cap', 'quarter results', 'annual results'],
    'Product Launch': ['launch', 'release', 'new product', 'announce product', 'unveil', 'showcase', 'introduce', 'develops'],
    'Market News': ['stock market', 'shares', 'trading', 'nasdaq', 'nyse', 'index', 'economy', 'market sentiment', 'analyst rating'],
    'Partnership & Deals': ['partner', 'collaboration', 'agreement', 'deal', 'acquisition', 'merger', 'investment', 'joint venture', 'acquires', 'invests in'],
    'Legal & Regulatory': ['lawsuit', 'regulation', 'compliance', 'investigation', 'sec', 'ftc', 'doj', 'settlement', 'court'],
    'Executive Changes': ['ceo', 'cfo', 'cto', 'board member', 'appoint', 'resign', 'hire', 'fire', 'executive appointment', 'management change'],
    'General Company News': ['company update', 'outlook', 'strategy', 'expansion', 'restructuring'] # Fallback category
}

def _load_zero_shot_model(model_name: str = DEFAULT_ZERO_SHOT_MODEL):
    global zero_shot_classifier
    if zero_shot_classifier is None:
        try:
            logger.info(f"Loading zero-shot classification model: {model_name}")
            zero_shot_classifier = pipeline(
                "zero-shot-classification",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info(f"Zero-shot classification model {model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading zero-shot model {model_name}: {e}", exc_info=True)
            zero_shot_classifier = None

def categorize_news_keyword(text: str, categories_keywords: Dict[str, List[str]] = None) -> Optional[str]:
    if categories_keywords is None:
        categories_keywords = DEFAULT_CATEGORIES_KEYWORDS

    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        logger.warning("Cannot categorize empty text (keyword).")
        return "Uncategorized"

    text_lower = text.lower()
    category_scores = {category: 0 for category in categories_keywords}

    for category, keywords in categories_keywords.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower): # Use word boundaries
                category_scores[category] += 1

    non_zero_scores = {cat: score for cat, score in category_scores.items() if score > 0}
    if not non_zero_scores:
        logger.info(f"No keywords matched for text (keyword): '{text[:100]}...'. Defaulting to 'General Company News'.")
        return "General Company News"

    best_category = max(non_zero_scores, key=non_zero_scores.get)
    logger.info(f"Keyword categorization for '{text[:50]}...': Best category='{best_category}'")
    return best_category

def categorize_news_zero_shot(text: str, candidate_labels: List[str], model_name: str = DEFAULT_ZERO_SHOT_MODEL, confidence_threshold: float = 0.6) -> Optional[str]:
    global zero_shot_classifier
    if zero_shot_classifier is None:
        _load_zero_shot_model(model_name)
        if zero_shot_classifier is None:
            logger.error("Zero-shot model not loaded. Cannot perform zero-shot categorization.")
            return None

    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        logger.warning("Cannot perform zero-shot categorization on empty text.")
        return None

    try:
        logger.debug(f"Performing zero-shot categorization on: '{text[:100]}...' with labels: {candidate_labels}")
        result = zero_shot_classifier(text, candidate_labels, truncation=True, multi_label=False)

        if result and 'labels' in result and 'scores' in result:
            best_label = result['labels'][0]
            best_score = result['scores'][0]
            logger.info(f"Zero-shot categorization for '{text[:50]}...': Label='{best_label}', Score: {best_score:.4f}")
            if best_score >= confidence_threshold:
                return best_label
            else:
                logger.info(f"Zero-shot top score {best_score:.4f} below threshold {confidence_threshold}.")
                return None
        else:
            logger.warning(f"Zero-shot classification did not return expected result for: {text[:50]}...")
            return None
    except Exception as e:
        logger.error(f"Error during zero-shot categorization: {e}", exc_info=True)
        return None

def categorize_news(text: str, use_zero_shot: bool = False, candidate_labels: Optional[List[str]] = None) -> Optional[str]:
    final_candidate_labels = candidate_labels if candidate_labels is not None else list(DEFAULT_CATEGORIES_KEYWORDS.keys())

    if use_zero_shot:
        logger.info("Attempting categorization with Zero-Shot model.")
        category = categorize_news_zero_shot(text, candidate_labels=final_candidate_labels)
        if category:
            return category
        logger.warning("Zero-shot categorization failed or below threshold, falling back to keyword-based.")

    logger.info("Using keyword-based categorization.")
    return categorize_news_keyword(text, categories_keywords=DEFAULT_CATEGORIES_KEYWORDS)

# --- Event Detection ---
DEFAULT_EVENT_PATTERNS = {
    "Earnings Report": [
        r'(reports|announces|releases|posts) (quarterly|q\d|annual|fiscal year|fy) (earnings|results|profit|revenue|loss)',
        r'(earnings|results) (beat|miss|exceed|fall short of) expectations',
        r'conference call to discuss (quarterly|q\d|annual|fy) results',
        r'eps (of|at|beats|misses)' # Earnings Per Share
    ],
    "Mergers & Acquisitions": [
        r'(acquires|buys|purchases|takes over) [A-Za-z0-9_.-]+', # Target company name
        r'[A-Za-z0-9_.-]+ to be acquired by',
        r'(merger|acquisition|takeover) (deal|agreement|talks|discussions|proposal|offer)',
        r'(agrees to|completes|finalizes|announces) (acquisition of|merger with)',
        r'buyout of'
    ],
    "Product Launch": [ # Can refine existing category keywords or add more specific event patterns
        r'(launches|unveils|introduces|releases|announces) (new|upcoming|next-gen|next generation) (product|service|platform|feature|software|hardware)',
        r'(product|service|platform) (now available|coming soon|beta version|to be released)',
        r'debuts (its|a) new'
    ],
    "Analyst Rating": [
        r'(analyst|firm|bank) (upgrades|downgrades|initiates|reiterates|maintains) (coverage|rating)',
        r'(price target|pt) (raised|lowered|set at|cut to)',
        r'(buy|sell|hold|overweight|underweight|neutral) rating'
    ],
    "Executive Change": [ # Similar to category, but more event-focused
        r'(appoints|names|hires) new (ceo|cfo|cto|coo|president|chairman|director|executive|officer|vp)',
        r'(ceo|cfo|cto|coo|president|chairman|director) (steps down|resigns|departs|retires|to leave)',
        r'leadership (change|transition|shakeup)'
    ]
}

def detect_events(text: str, event_patterns: Dict[str, List[str]] = None) -> List[str]:
    if event_patterns is None:
        event_patterns = DEFAULT_EVENT_PATTERNS

    detected_event_types = []
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        logger.warning("Cannot detect events in empty text.")
        return detected_event_types

    text_lower = text.lower() # Some regex patterns might be case-insensitive, but good to normalize

    for event_type, patterns in event_patterns.items():
        for pattern in patterns:
            # Using re.IGNORECASE for flexibility with capitalization in news
            if re.search(pattern, text, re.IGNORECASE):
                if event_type not in detected_event_types: # Add only once
                    detected_event_types.append(event_type)
                # Found a match for this event type, can break from inner loop (patterns for this event)
                # Or continue if multiple patterns for the same event type might indicate stronger signal (not implemented here)
                break

    if detected_event_types:
        logger.info(f"Detected events for '{text[:50]}...': {detected_event_types}")
    else:
        logger.info(f"No specific events detected for '{text[:50]}...'.")

    return detected_event_types
