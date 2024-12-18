from playwright.sync_api import sync_playwright, Browser, Page
import random
import logging
from src.config.config import Config

logger = logging.getLogger(__name__)

class PlaywrightDriver:
    """
    A context manager for managing a Playwright browser session.

    Attributes:
        proxy (str): Proxy server address.
        headless (bool): Whether to run the browser in headless mode.
    """

    def __init__(self, proxy: str = None, headless: bool = True):
        self.proxy = proxy
        self.headless = headless
        self.browser: Browser = None
        self.context = None
        self.page: Page = None

    def __enter__(self) -> Page:
        """
        Start the Playwright session and open a new page.

        Returns:
            Page: A new page instance.
        """
        try:
            self.pw = sync_playwright().start()
            browser_args = {
                "headless": self.headless
            }
            if self.proxy:
                browser_args["proxy"] = {"server": self.proxy}
            self.browser = self.pw.chromium.launch(**browser_args)
            self.context = self.browser.new_context(
                user_agent=random.choice(Config.USER_AGENTS)
            )
            self.page = self.context.new_page()
            logger.info("Playwright session started successfully.")
            return self.page
        except Exception as e:
            logger.error(f"Failed to start Playwright session: {e}")
            self.__exit__(None, None, None)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the Playwright session, releasing all resources.
        """
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.pw:
                self.pw.stop()
            logger.info("Playwright session closed successfully.")
        except Exception as e:
            logger.error(f"Error closing Playwright session: {e}") 