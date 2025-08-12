# -*- coding: utf-8 -*-
"""
Utility for performing semantic search using Hugging Face Inference API.
"""
import requests
from config import HUGGINGFACE_API_KEY
from utils.logger import get_logger

logger = get_logger(__name__)

# Recommended model for sentence similarity
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def get_sentence_similarity_scores(source_sentence: str, sentences_to_compare: list[str]) -> list[float] | None:
    """
    Uses the Hugging Face Inference API to get similarity scores between a source
    sentence and a list of other sentences.

    Args:
        source_sentence: The user's new question.
        sentences_to_compare: A list of existing questions from the FAQ.

    Returns:
        A list of float scores, corresponding to the sentences_to_compare list, or None on error.
    """
    if not HUGGINGFACE_API_KEY:
        logger.info("HUGGINGFACE_API_KEY not set. Skipping semantic search.")
        return None

    try:
        payload = {
            "inputs": {
                "source_sentence": source_sentence,
                "sentences": sentences_to_compare
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)

        if response.status_code != 200:
            logger.error(f"Hugging Face API request failed with status {response.status_code}: {response.text}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Hugging Face API: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred in semantic search: {e}")
        return None
