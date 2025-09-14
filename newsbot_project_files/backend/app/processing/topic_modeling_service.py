from bertopic import BERTopic
from typing import List, Optional, Union
import torch
from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

DEFAULT_TOPIC_MODEL = "MaartenGr/BERTopic_Wikipedia"
topic_model = None

def _load_topic_model(model_name: str = DEFAULT_TOPIC_MODEL):
    global topic_model
    if topic_model is None:
        try:
            logger.info(f"Loading topic modeling model: {model_name}")
            # BERTopic handles device placement automatically with 'auto'
            topic_model = BERTopic.load(model_name)
            logger.info(f"Topic modeling model {model_name} loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading topic model {model_name}: {e}", exc_info=True)
            topic_model = None

def get_topics(docs: Union[str, List[str]], model_name: str = DEFAULT_TOPIC_MODEL) -> Optional[dict]:
    global topic_model
    if topic_model is None:
        _load_topic_model(model_name)
        if topic_model is None:
            logger.error("Topic model could not be loaded. Cannot perform topic modeling.")
            return None

    if not docs or (isinstance(docs, list) and not docs):
        logger.warning("Cannot perform topic modeling on empty input.")
        return {"topics": [], "probabilities": [], "error": "Empty input"}

    try:
        logger.debug(f"Performing topic modeling on {len(docs)} documents.")
        # The `transform` method can take a single doc or a list of docs
        topics, probs = topic_model.transform(docs)

        # Get topic representations
        topic_labels = [topic_model.topic_labels_.get(t, f"Topic {t}") for t in topics]

        logger.info(f"Identified topics for {len(docs)} documents.")
        return {"topics": topics, "probabilities": probs, "topic_labels": topic_labels}
    except Exception as e:
        logger.error(f"Error during topic modeling: {e}", exc_info=True)
        return {"topics": [], "probabilities": [], "error": str(e)}

def get_main_topics(docs: List[str], top_n: int = 5, model_name: str = DEFAULT_TOPIC_MODEL) -> Optional[dict]:
    """
    A convenience function to get the most frequent topics from a list of documents.
    """
    global topic_model
    if topic_model is None:
        _load_topic_model(model_name)
        if topic_model is None:
            return None

    if not docs or not isinstance(docs, list) or len(docs) == 0:
        logger.warning("Cannot perform topic modeling on empty list of documents.")
        return {"top_topics": [], "error": "Empty input"}

    try:
        # The fit_transform method is used to both fit the model and transform the docs.
        # This is more suitable for finding topics in a batch of documents.
        topics, _ = topic_model.fit_transform(docs)

        # Get the most frequent topics
        frequent_topics = topic_model.get_topic_info().head(top_n + 1) # +1 to account for the outlier topic (-1)

        # Filter out the outlier topic if it's present
        if frequent_topics.iloc[0]["Topic"] == -1:
            frequent_topics = frequent_topics.iloc[1:]
        else:
            frequent_topics = frequent_topics.head(top_n)

        top_topics_dict = frequent_topics.to_dict(orient='records')

        logger.info(f"Identified top {top_n} topics from {len(docs)} documents.")
        return {"top_topics": top_topics_dict}
    except Exception as e:
        logger.error(f"Error during main topic identification: {e}", exc_info=True)
        return {"top_topics": [], "error": str(e)}
