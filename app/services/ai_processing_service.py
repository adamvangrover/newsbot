import logging
from typing import Optional
from app.models.schemas import SentimentOutput, CategoryOutput # Ensure CategoryOutput is imported
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch 

# Configure logging
logger = logging.getLogger(__name__)

class AIProcessingService:
    SENTIMENT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

    # Basic Keyword-based Categorization
    KEYWORD_CATEGORIES = {
        "Earnings": ["earnings", "profit", "revenue", "financial results", "quarterly report", "annual report", "EPS", "net income"],
        "Partnership": ["partner", "partnership", "collaboration", "agreement", "alliance", "joint venture", "team up"],
        "Product": ["product launch", "new release", "feature update", "launches", "unveils", "introduces new product", "software update", "hardware release"],
        "Market News": ["stock price", "market cap", "shares", "analyst rating", "upgrade", "downgrade", "acquisition", "merger", "ipo"],
        # Add more categories and keywords as needed
    }
    DEFAULT_CATEGORY = "General News"

    def __init__(self):
        try:
            device = 0 if torch.cuda.is_available() else -1 
            logger.info(f"Initializing sentiment analysis pipeline on device: {'cuda' if device == 0 else 'cpu'}")
            
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.SENTIMENT_MODEL_NAME,
                device=device 
            )
            logger.info(f"Sentiment analysis pipeline loaded successfully with model: {self.SENTIMENT_MODEL_NAME}")

        except Exception as e:
            logger.error(f"Error initializing Hugging Face sentiment pipeline: {e}", exc_info=True)
            self.sentiment_pipeline = None 
    
    def get_sentiment(self, text: str) -> Optional[SentimentOutput]:
        if not self.sentiment_pipeline:
            logger.error("Sentiment pipeline not available. Cannot process sentiment.")
            return None
        if not text or not isinstance(text, str) or not text.strip():
            logger.warning("Cannot get sentiment for empty or invalid text.")
            return None

        try:
            results = self.sentiment_pipeline(text, truncation=True, max_length=510) 
            
            if results and isinstance(results, list) and len(results) > 0:
                result = results[0] 
                label = result.get("label")
                score = result.get("score")
                return SentimentOutput(label=label.upper(), score=score)
            else:
                logger.warning(f"Sentiment analysis for text '{text[:50]}...' returned no valid results.")
                return None
        except Exception as e:
            logger.error(f"Error during sentiment analysis for text '{text[:50]}...': {e}", exc_info=True)
            return None

    def get_category(self, text: str) -> Optional[CategoryOutput]: # Added Optional for consistency, though current logic always returns
        if not text or not isinstance(text, str) or not text.strip():
            logger.warning("Cannot get category for empty or invalid text.")
            # Return default category for empty/invalid text, or None if preferred
            return CategoryOutput(label=self.DEFAULT_CATEGORY) 

        lower_text = text.lower()
        
        for category, keywords in self.KEYWORD_CATEGORIES.items():
            for keyword in keywords:
                if keyword in lower_text:
                    return CategoryOutput(label=category)
        
        return CategoryOutput(label=self.DEFAULT_CATEGORY)

# Example Usage (for local testing)
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     
#     print("Initializing AIProcessingService...")
#     ai_service = AIProcessingService()
#     print("AIProcessingService initialized.")

#     if ai_service.sentiment_pipeline: 
#         texts_to_analyze = [
#             "This is a fantastic product! I love it.",
#             "The new update is terrible and broke everything.",
#             "The company announced positive earnings.",
#             "Market sentiment is rather neutral today.",
#             "Despite some concerns, the outlook is generally good.",
#             "The company reported strong quarterly earnings.", # New example for categorization
#             "A new strategic partnership was announced today.", # New example
#             "They are launching a new phone next month."      # New example
#         ]
#         for text_content in texts_to_analyze:
#             print(f"\nAnalyzing: '{text_content}'")
#             sentiment = ai_service.get_sentiment(text_content)
#             if sentiment:
#                 print(f"-> Sentiment: Label={sentiment.label}, Score={sentiment.score:.4f}")
#             else:
#                 print("-> Could not determine sentiment.")
#
#             category_obj = ai_service.get_category(text_content) # Test categorization
#             if category_obj:
#                 print(f"-> Category: {category_obj.label}")
#             else: # Should not happen with current get_category logic but good practice
#                 print("-> Could not determine category.")
#     else:
#         print("Sentiment analysis pipeline could not be initialized. Cannot run example.")
