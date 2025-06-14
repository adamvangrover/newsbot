from typing import List, Dict, Optional
from newsbot_project_files.backend.app.schemas.news import NewsArticle
from newsbot_project_files.backend.app.core.logging import get_logger
from newsbot_project_files.backend.app.processing.sentiment import get_sentiment
from newsbot_project_files.backend.app.processing.categorization import categorize_news, DEFAULT_CATEGORIES_KEYWORDS
from newsbot_project_files.backend.app.processing.summarization import summarize_text

logger = get_logger(__name__)

class AIProcessingService:

    def __init__(self):
        # Models are loaded lazily by the processing functions on first use.
        logger.info("AIProcessingService initialized. Models will be loaded on first use.")

    async def process_news_articles(self, articles: List[NewsArticle]) -> List[NewsArticle]:
        processed_articles: List[NewsArticle] = []

        # For MVP, let's set zero-shot to False. Can be a config option later.
        use_zero_shot_categorization = False
        candidate_category_labels = list(DEFAULT_CATEGORIES_KEYWORDS.keys())

        for article in articles:
            try:
                logger.info(f"Processing article ID: {article.id} - {article.headline[:100]}...")
                # Use headline and summary for more comprehensive analysis
                text_for_analysis = f"{article.headline}. {article.summary}"

                # 1. Sentiment Analysis
                sentiment_result = get_sentiment(text_for_analysis)
                if sentiment_result:
                    article.sentiment_label = sentiment_result.get('label')
                    article.sentiment_score = sentiment_result.get('score')
                    if sentiment_result.get('error'): # Check if an error message was returned
                         logger.warning(f"Sentiment analysis for article {article.id} had an issue: {sentiment_result.get('error')}")
                else:
                    logger.warning(f"Sentiment analysis failed or returned None for article {article.id}")
                    article.sentiment_label = "Unavailable"
                logger.debug(f"Article {article.id} sentiment: {article.sentiment_label} (Score: {article.sentiment_score})")

                # 2. News Categorization
                article.analyzed_category = categorize_news(
                    text_for_analysis,
                    use_zero_shot=use_zero_shot_categorization,
                    candidate_labels=candidate_category_labels
                )
                logger.debug(f"Article {article.id} AI category: {article.analyzed_category}")

                # 3. Summarization
                # Decide what text to summarize. If original summary is very short, AI summary might not be better.
                # If original summary is long, AI summary is useful.
                text_to_summarize = article.summary
                if not text_to_summarize or len(text_to_summarize.strip().split()) < 20: # If summary is less than 20 words
                    logger.info(f"Original summary for article {article.id} is short. AI summary might not be generated or may use headline.")
                    # Optionally, could try to summarize article.headline if summary is too short.
                    # For now, if summary is too short, AI summary might just return the original short summary.
                    # Or we can choose not to generate one.
                    article.ai_summary = article.summary # Keep original if too short. Summarize function handles this.

                # The summarize_text function itself checks for short text.
                ai_generated_summary = summarize_text(text_to_summarize)
                if ai_generated_summary and "Error in summarization" not in ai_generated_summary:
                    article.ai_summary = ai_generated_summary
                    logger.debug(f"Article {article.id} AI summary generated (first 50 chars): {article.ai_summary[:50]}...")
                elif ai_generated_summary and "Error in summarization" in ai_generated_summary:
                    logger.warning(f"AI summarization for article {article.id} encountered an error: {ai_generated_summary}")
                    article.ai_summary = article.summary # Fallback to original summary
                else: # summarize_text returned None or original short text
                    logger.warning(f"AI summarization did not produce a new summary for article {article.id}. Original summary: '{article.summary[:50]}...'")
                    article.ai_summary = article.summary # Fallback or keep as is

                processed_articles.append(article)
            except Exception as e:
                logger.error(f"Major error processing article {article.id} ('{article.headline[:50]}...'): {e}", exc_info=True)
                # Fallback: append original article with error indicators
                article.sentiment_label = article.sentiment_label or "Processing Error"
                article.analyzed_category = article.analyzed_category or "Processing Error"
                article.ai_summary = article.ai_summary or "Processing Error"
                processed_articles.append(article)

        logger.info(f"AI Service: Processed {len(processed_articles)} articles.")
        return processed_articles
