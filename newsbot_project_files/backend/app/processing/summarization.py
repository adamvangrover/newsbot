from transformers import pipeline
from typing import Optional
import torch

from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

DEFAULT_SUMMARIZATION_MODEL = "t5-small" # Small and fast, decent quality for MVP
summarizer = None

def _load_summarization_model(model_name: str = DEFAULT_SUMMARIZATION_MODEL):
    global summarizer
    if summarizer is None:
        try:
            logger.info(f"Loading summarization model: {model_name}")
            summarizer = pipeline(
                "summarization",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info(f"Summarization model {model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading summarization model {model_name}: {e}", exc_info=True)
            summarizer = None

def summarize_text(text: str, model_name: str = DEFAULT_SUMMARIZATION_MODEL, min_length: int = 20, max_length_ratio: float = 0.5) -> Optional[str]:
    global summarizer
    if summarizer is None:
        _load_summarization_model(model_name)
        if summarizer is None:
            logger.error("Summarization model not loaded. Cannot perform summarization.")
            return None

    if not text or not isinstance(text, str) or len(text.strip()) < 30 : # Need some meaningful text, e.g. >30 chars
        logger.warning(f"Text too short or empty for summarization ('{text[:30]}...'). Returning original text.")
        return text

    try:
        # Calculate max_length based on ratio of original text, but cap it to avoid being too long.
        # The model itself has a max input token limit (e.g. 512 or 1024 for t5-small's encoder)
        # The pipeline should handle truncation of input.
        # We set max_length for the *output* summary.
        # Ensure max_length is not less than min_length.
        estimated_max_length = int(len(text.split()) * max_length_ratio) # Based on word count
        actual_max_length = max(min_length + 5, min(estimated_max_length, 150)) # Cap at 150 words, ensure min_length < max_length
        if actual_max_length <= min_length :
             actual_max_length = min_length + 10 # ensure max is greater than min

        logger.debug(f"Performing summarization on text (length {len(text)} chars)... Target min/max: {min_length}/{actual_max_length} words.")

        # `truncation=True` is important for the pipeline to handle inputs longer than model's capacity
        result = summarizer(text, min_length=min_length, max_length=actual_max_length, truncation=True, do_sample=False)

        if result and isinstance(result, list) and 'summary_text' in result[0]:
            summary = result[0]['summary_text']
            logger.info(f"Summarized text (original {len(text)} chars) to (summary {len(summary)} chars): '{summary[:100]}...'")
            return summary.strip()
        else:
            logger.warning(f"Summarization did not return expected result for text: {text[:50]}...")
            return None
    except Exception as e:
        logger.error(f"Error during summarization for text '{text[:50]}...': {e}", exc_info=True)
        return f"Error in summarization: {str(e)}" # Return error message in summary
