import httpx # Using httpx for async requests
from bs4 import BeautifulSoup, NavigableString, Comment
from typing import Optional, Tuple
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError

from newsbot_project_files.backend.app.core.logging import get_logger

logger = get_logger(__name__)

class WebScrapingService:
    def __init__(self, timeout: int = 15):
        self.default_timeout = timeout

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(2), reraise=True)
    async def fetch_url_content(self, url: str) -> Optional[str]:
        """Fetches HTML content from a given URL."""
        try:
            async with httpx.AsyncClient(timeout=self.default_timeout, follow_redirects=True) as client:
                # Using a common user-agent to mimic a browser
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                logger.info(f"Fetching URL: {url}")
                response = await client.get(url, headers=headers)
                response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses

                # Check content type to ensure it's likely HTML/text
                content_type = response.headers.get("content-type", "").lower()
                if not ("html" in content_type or "text" in content_type or "xml" in content_type):
                    logger.warning(f"URL {url} returned non-HTML/text content-type: {content_type}. May not be scrapable.")
                    # Depending on strictness, could return None or error here

                logger.debug(f"Successfully fetched content from {url}. Content length: {len(response.text)} bytes.")
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} while fetching {url}: {e.response.text[:200]}")
            # For client errors like 404, 403, no point in retrying usually.
            # Tenacity handles retries for server errors or transient network issues.
            if 400 <= e.response.status_code < 500:
                 raise # Reraise to stop tenacity if it's a client error not worth retrying by default.
            # Otherwise, let tenacity decide based on its config.
            return None # Or re-raise e if tenacity should handle it
        except httpx.RequestError as e: # Covers network errors, timeouts, etc.
            logger.error(f"Request error while fetching {url}: {e}")
            raise # Reraise to allow tenacity to handle retries
        except Exception as e:
            logger.error(f"Unexpected error fetching URL {url}: {e}", exc_info=True)
            return None

    def extract_main_text_content(self, html_content: str, url: str = "") -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the main text content and title from HTML.
        Tries to remove boilerplate like nav, footer, ads, scripts, styles.
        Returns a tuple: (main_text, title)
        """
        if not html_content:
            return None, None

        try:
            soup = BeautifulSoup(html_content, 'lxml') # lxml is generally faster

            page_title = soup.title.string if soup.title else None
            logger.debug(f"Page title for {url if url else 'source'}: {page_title}")

            # Remove script, style, head, nav, footer, header, aside, form, comments
            tags_to_remove = ['script', 'style', 'head', 'nav', 'footer', 'header', 'aside', 'form', 'noscript', 'iframe', 'svg', 'path']
            for tag_name in tags_to_remove:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # Remove comments
            for element in soup(text=lambda text: isinstance(text, Comment)):
                element.extract()

            # Attempt to find main content containers (common tags/attributes)
            # This is heuristic and might need adjustment for specific site structures
            main_content_selectors = [
                'article', 'main',
                '[role="main"]',
                '.post-content', '.entry-content', '.content', '.main-content', '.story-content', # common class names
                '#article-body', '#main-content', '#content' # common ids
            ]

            main_text_element = None
            for selector in main_content_selectors:
                main_text_element = soup.select_one(selector)
                if main_text_element:
                    logger.debug(f"Found main content element for {url} using selector: {selector}")
                    break

            if not main_text_element:
                logger.info(f"No specific main content element found for {url}. Using body as fallback.")
                main_text_element = soup.body
                if not main_text_element: # Should not happen if body exists
                    logger.warning(f"No body tag found for {url}. Cannot extract text.")
                    return None, page_title


            # Get text, joining paragraphs with newlines for better readability
            # and to help NLP models understand structure.
            text_parts = []
            for element in main_text_element.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td']):
                # Filter out elements that are likely not main content based on heuristics
                # (e.g., very short, hidden, or typically boilerplate class names)
                class_str = ' '.join(element.get('class', [])).lower()
                id_str = element.get('id', '').lower()

                # Skip common boilerplate patterns - this list can be expanded
                boilerplate_patterns = ['ad', 'advert', 'banner', 'button', 'comment', 'cookie', 'related', 'share', 'social', 'sidebar', 'widget', 'menu', 'nav', 'footer', 'header', 'hidden', 'modal', 'popup']

                skip = False
                for pattern in boilerplate_patterns:
                    if pattern in class_str or pattern in id_str:
                        skip = True
                        break
                if skip:
                    continue

                # Get text from the element, stripping leading/trailing whitespace
                text = element.get_text(separator=' ', strip=True)
                if text:
                    text_parts.append(text)

            if not text_parts: # Fallback if specific element search yields nothing
                 logger.info(f"No text parts found in main element for {url}, falling back to all text from main_text_element or body.")
                 text_content = main_text_element.get_text(separator='\n', strip=True)
            else:
                 text_content = "\n\n".join(text_parts) # Join paragraphs with double newlines

            # Basic cleaning: remove excessive newlines and whitespace
            text_content = '\n'.join([line.strip() for line in text_content.splitlines() if line.strip()])
            text_content = text_content.replace('\n\n\n', '\n\n') # Reduce triple newlines to double

            if not text_content.strip():
                logger.warning(f"Extracted text content is empty for {url} after cleaning.")
                return None, page_title

            logger.info(f"Successfully extracted text content from {url if url else 'source'}. Length: {len(text_content)} chars.")
            return text_content, page_title

        except Exception as e:
            logger.error(f"Error parsing HTML content for {url if url else 'source'}: {e}", exc_info=True)
            return None, None # Return None for text, None for title on error

    async def scrape_article_text(self, url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        High-level method to fetch and extract main text content and title from a URL.
        Returns (text_content, page_title, error_message)
        """
        html_content = None
        error_message = None
        try:
            html_content = await self.fetch_url_content(url)
            if not html_content:
                logger.warning(f"Failed to fetch HTML content from {url}.")
                return None, None, "Failed to fetch HTML content."
        except RetryError as re:
            logger.error(f"Max retries exceeded for fetching URL {url}: {re}")
            return None, None, f"Failed to fetch URL after multiple retries: {re}"
        except httpx.HTTPStatusError as hse: # Catching specific client errors that stop retries
            logger.error(f"HTTP client error fetching URL {url}: {hse.response.status_code}")
            return None, None, f"HTTP error {hse.response.status_code} fetching URL."
        except Exception as e: # Catch-all for other fetch errors
            logger.error(f"Generic error fetching URL {url}: {e}", exc_info=True)
            return None, None, f"Error fetching URL: {str(e)}"


        text_content, page_title = self.extract_main_text_content(html_content, url=url)
        if not text_content:
            logger.warning(f"Failed to extract text content from {url}.")
            return None, page_title, error_message or "Failed to extract text content."

        return text_content, page_title, None


# Example usage (for testing this service directly)
if __name__ == "__main__":
    import asyncio

    async def main():
        service = WebScrapingService()
        # test_url = "https://www.bbc.com/news/world-us-canada-60288000" # Example, might change
        test_url = "https://www.example.com" # More stable

        print(f"--- Testing with URL: {test_url} ---")
        text, title, error = await service.scrape_article_text(test_url)

        if error:
            print(f"Error: {error}")
        if title:
            print(f"Title: {title}")
        if text:
            print(f"\nExtracted Text (first 500 chars):\n{text[:500]}")

        print(f"\n--- Testing with non-HTML URL ---")
        non_html_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        text_png, title_png, error_png = await service.scrape_article_text(non_html_url)
        if error_png:
            print(f"Error for PNG: {error_png}")
        if title_png:
             print(f"Title for PNG: {title_png}")
        if text_png:
            print(f"Text for PNG: {text_png}")

        print(f"\n--- Testing with invalid URL ---")
        invalid_url = "http://thissitedoesnotexist12345.com"
        text_invalid, title_invalid, error_invalid = await service.scrape_article_text(invalid_url)
        if error_invalid:
            print(f"Error for invalid URL: {error_invalid}")
        if title_invalid:
            print(f"Title for invalid URL: {title_invalid}")

    asyncio.run(main())
