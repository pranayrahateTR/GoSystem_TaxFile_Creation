import logging

import allure
from playwright.sync_api import expect

from pages.BasePage import BasePage
from pages.EnterDetailsPage import EnterDetailsPage
from utilities.generate_log import Logger

log = Logger(__name__, logging.DEBUG)


class ReturnsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

#_________________________Create New Returns___________________________#
    def create_new_Return(self):
        log.logger.info("Clicking Create New Return button")
        self.click("create_return_btn")
        return self

    def Fill_details(self, Year, Type, Fname, Lname):
        log.logger.info(f"Filling return details — Year: {Year}, Type: {Type}, Fname: {Fname}, Lname: {Lname}")
        with allure.step(f"Filling details for Taxpayer"):
            # select Tax Year
            self.type("select_year", str(Year))
            self.wait_for_load_state("domcontentloaded")
            # select return Type
            self.type("Select Type", str(Type))
            # Enter Taxpayer info
            self.type("fname_css", Fname)
            self.type("lname_css", Lname)
            self.click("checkbox_css")
            self.is_checked("checkbox_css")
            self.click("create_btn")
            self.wait_for_load_state("networkidle")
            log.logger.info("Return details filled and form submitted")
            return self

#__________________Select Mode________________#

    def Select_Mode(self):
        with allure.step("Selecting user mode from popup"):
            try:
                self.wait_for_element("single_user", state="visible", timeout=5000)
                log.logger.info("First return in session: selecting single user mode")
                # First return in session: popup appears, select mode and open new tab
                self.click("single_user")
                self.click_and_switch_to_new_tab("continue_btn")
            except Exception:
                log.logger.info("Subsequent return: mode already saved, waiting for new tab")
                # Subsequent returns: mode already saved, new tab opens automatically
                self.wait_for_new_tab_and_switch()
            self.wait_for_load_state("networkidle")
            log.logger.info("Mode selected, switching to EnterDetailsPage")
            ogpage = EnterDetailsPage(self.page)
            ogpage.original_page = self.original_page
            return ogpage


