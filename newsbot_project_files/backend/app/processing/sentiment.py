from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Optional
import torch # PyTorch is a dependency for Hugging Face transformers

from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

DEFAULT_SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = None
# Optional: For manual loading if pipeline is not used
# sentiment_tokenizer = None
# sentiment_model = None

def _load_sentiment_model(model_name: str = DEFAULT_SENTIMENT_MODEL):
    global sentiment_analyzer #, sentiment_tokenizer, sentiment_model
    if sentiment_analyzer is None:
        try:
            logger.info(f"Loading sentiment analysis model: {model_name}")
            sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1 # Use GPU if available, else CPU
            )
            logger.info(f"Sentiment analysis model {model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading sentiment model {model_name}: {e}", exc_info=True)
            sentiment_analyzer = None

def get_sentiment(text: str, model_name: str = DEFAULT_SENTIMENT_MODEL) -> Optional[Dict[str, any]]:
    global sentiment_analyzer
    if sentiment_analyzer is None:
        _load_sentiment_model(model_name)
        if sentiment_analyzer is None:
            logger.error("Sentiment model could not be loaded. Cannot perform sentiment analysis.")
            return None

    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        logger.warning("Cannot perform sentiment analysis on empty text.")
        return {"label": "NEUTRAL", "score": 0.0, "error": "Empty input"}

    try:
        # Pipeline handles truncation if text is too long for the model
        logger.debug(f"Performing sentiment analysis on: '{text[:100]}...'")
        result = sentiment_analyzer(text, truncation=True)

        if result and isinstance(result, list):
            analysis = result[0]
            logger.info(f"Sentiment for '{text[:50]}...': {analysis['label']}, Score: {analysis['score']:.4f}")
            return {"label": analysis["label"].upper(), "score": round(analysis["score"], 4)}
        else:
            logger.warning(f"Sentiment analysis did not return expected result for: {text[:50]}...")
            return None
    except Exception as e:
        logger.error(f"Error during sentiment analysis for text '{text[:50]}...': {e}", exc_info=True)
        return {"label": "ERROR", "score": 0.0, "error": str(e)}
