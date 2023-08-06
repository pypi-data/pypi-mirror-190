from playwright.sync_api import sync_playwright
from robotlibcore import keyword
from .custom_locator import *


def _get_playwright_context_manager():
    if not BaseContext.playwright_context_manager:
        BaseContext.playwright_context_manager = sync_playwright().start()
    return BaseContext.playwright_context_manager


CHROME_OPTIONS = ["--ignore-certificate-errors", "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                 "AppleWebKit/537.36 "
                                                 "(KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"]

TIMEOUT = 45000
SMALL_TIMEOUT = 15000
BROWSER = "chrome"
HEADLESS_MODE = True


class BaseContext:

    playwright_context_manager = None

    def __init__(self):
        self.player = _get_playwright_context_manager()

    @keyword("close all browsers")
    def close_all_browsers(self):
        self.player.stop()

    def _setup_custom_locators(self):
        self.player.selectors.register('item', QUERY_BY_ITEM)
        self.player.selectors.register('btn', QUERY_BY_BTN)
        self.player.selectors.register('plc', QUERY_BY_PLC)
        self.player.selectors.register('cbx', QUERY_BY_CBX)
        self.player.selectors.register('radio', QUERY_BY_RADIO)
        self.player.selectors.register('link', QUERY_BY_LINK)
        self.player.selectors.register('name', QUERY_BY_NAME)
        self.player.selectors.register('class', QUERY_BY_CLASS)
