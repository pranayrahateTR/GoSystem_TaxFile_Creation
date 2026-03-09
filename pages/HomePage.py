import logging
import time

import allure
from playwright.sync_api import sync_playwright, expect
import pytest

from pages.BasePage import BasePage
from pages.ReturnsPage import ReturnsPage
from utilities import configReader
from utilities.generate_log import Logger

log = Logger(__name__, logging.DEBUG)


class CreateNewReturn(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def select_createReturn(self):
        with allure.step("Navigating to Create New Return page"):
            log.logger.info("Navigating to Create New Return page")
            self.verify_element_visible("returns_id", timeout=5000)
            self.click("returns_id")
            log.logger.info("Returns page opened")
            return ReturnsPage(self.page)

    def select_mode(self):
        with allure.step("Selecting Mode"):
            log.logger.info("Selecting mode")
            self.click("select_mode")


