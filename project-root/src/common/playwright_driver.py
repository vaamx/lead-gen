from playwright.sync_api import sync_playwright
import random
from src.config.config import Config

class PlaywrightDriver:
    def __init__(self, proxy=None, headless=True):
        self.proxy = proxy
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
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
        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.context.close()
        self.browser.close()
        self.pw.stop() 