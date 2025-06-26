from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from typing import List, Dict, Optional
import torch

from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

DEFAULT_NER_MODEL = "dslim/bert-base-NER"
ner_pipeline = None

# Mapping from model labels to more common labels if needed, or for grouping
# dslim/bert-base-NER uses standard CoNLL-2003 labels:
# ORG: Organization
# PER: Person
# LOC: Location
# MISC: Miscellaneous
ENTITY_LABEL_MAP = {
    "O": "Outside", # Typically filtered out
    "B-MISC": "Miscellaneous",
    "I-MISC": "Miscellaneous",
    "B-PER": "Person",
    "I-PER": "Person",
    "B-ORG": "Organization",
    "I-ORG": "Organization",
    "B-LOC": "Location",
    "I-LOC": "Location",
}

def _load_ner_model(model_name: str = DEFAULT_NER_MODEL):
    global ner_pipeline
    if ner_pipeline is None:
        try:
            logger.info(f"Loading NER model: {model_name}")
            # It's good practice to load tokenizer and model separately for some configurations,
            # but pipeline usually handles it. Using explicit model and tokenizer for clarity.
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTokenClassification.from_pretrained(model_name)
            ner_pipeline = pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                device=0 if torch.cuda.is_available() else -1,
                # Group entities for models that support it (like dslim/bert-base-NER)
                # This combines B-ORG and I-ORG into a single "Apple Inc." entity
                aggregation_strategy="simple"
            )
            logger.info(f"NER model {model_name} loaded successfully with aggregation_strategy='simple'.")
        except Exception as e:
            logger.error(f"Error loading NER model {model_name}: {e}", exc_info=True)
            ner_pipeline = None

def extract_entities(text: str, model_name: str = DEFAULT_NER_MODEL, confidence_threshold: float = 0.85) -> Optional[List[Dict[str, any]]]:
    global ner_pipeline
    if ner_pipeline is None:
        _load_ner_model(model_name)
        if ner_pipeline is None:
            logger.error("NER model could not be loaded. Cannot perform entity extraction.")
            return None

    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        logger.warning("Cannot perform NER on empty text.")
        return []

    try:
        logger.debug(f"Performing NER on: '{text[:100]}...'")
        # The pipeline with aggregation_strategy="simple" returns a list of dicts:
        # [{'entity_group': 'ORG', 'score': 0.99, 'word': 'Apple', 'start': 0, 'end': 5}, ...]
        raw_entities = ner_pipeline(text, truncation=True)

        processed_entities = []
        if raw_entities:
            for entity in raw_entities:
                if entity.get('score', 0) >= confidence_threshold:
                    processed_entity = {
                        "text": entity.get("word"),
                        "label": entity.get("entity_group"), # Using entity_group from aggregation
                        "score": round(float(entity.get("score")), 4),
                        "start_offset": entity.get("start"),
                        "end_offset": entity.get("end")
                    }
                    processed_entities.append(processed_entity)

            logger.info(f"Extracted {len(processed_entities)} entities from '{text[:50]}...' (threshold {confidence_threshold})")
            return processed_entities
        else:
            logger.info(f"No entities found by NER pipeline for: {text[:50]}...")
            return []

    except Exception as e:
        logger.error(f"Error during NER for text '{text[:50]}...': {e}", exc_info=True)
        return None # Indicate error, distinct from empty list

# Example usage (for testing)
if __name__ == "__main__":
    sample_text = "Apple Inc. is planning to build a new factory in Austin, Texas. Tim Cook announced this yesterday."
    entities = extract_entities(sample_text)
    if entities:
        for ent in entities:
            print(f"Entity: {ent['text']}, Type: {ent['label']}, Score: {ent['score']}")

    sample_text_2 = "Microsoft announced a new partnership with NVIDIA to advance AI research in their Redmond campus."
    entities_2 = extract_entities(sample_text_2)
    if entities_2:
        for ent in entities_2:
            print(f"Entity: {ent['text']}, Type: {ent['label']}, Score: {ent['score']}")

    empty_text = ""
    entities_empty = extract_entities(empty_text)
    print(f"Entities from empty text: {entities_empty}")

    short_text = "Hello world."
    entities_short = extract_entities(short_text)
    print(f"Entities from short text: {entities_short}")
