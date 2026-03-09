import logging

import allure
from logging import log
from utilities.generate_log import Logger
from pages.BasePage import BasePage

log1=Logger(__name__,logging.DEBUG)

class EnterDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def getLcoatorId(self):
        with allure.step("Getting Locator ID"):
            locator = self.get_text("locator_id")
            get_locator = locator.split('|')[2].strip()
        log1.logger.info(f"Captured Locator: {get_locator}")
        return get_locator

    def EnterDetails(self,SSN:str,DOB:str,Address1:str,Address2:str,Apartment:str,City:str,County:str,State:str,Zip:str ):
        with allure.step(f"Entering taxpayer details — SSN: {SSN}, DOB: {DOB},Address1: {Address1},Address2: {Address2},Apartment: {Apartment},City: {City},Country: {County},State: {State},Zip: {Zip}"):
            log1.logger.info(f"Entering taxpayer details — SSN: {SSN}, DOB: {DOB},Address1: {Address1},Address2: {Address2},Apartment: {Apartment},City: {City},Country: {County},State: {State},Zip: {Zip}")

            self.captured_locator_id = self.getLcoatorId()
            self.click_by_text("general_info_txt")
            self.click_by_text("basic_return_info")
            self.click_by_text("Taxpayer_info")
            self.select_custom_dropdown("Filling_state", "Single")
            self.field_is_editable("SSN")
            self.type("SSN", SSN)
            self.field_is_editable("SSN")
            self.type("DOB", DOB)

            # Address Details
            log1.logger.info(f"Filling address — {Address1}, {Address2}, {Apartment}, {City}, {County}, {State}, {Zip}")
            self.type("Address1", Address1)
            self.type("Address2", Address2)
            self.type("Apartment", Apartment)
            self.type("city", City)
            self.type("county", County)
            self.select_custom_dropdown("state", State)
            self.type("zip", Zip)
            self.click("compute")
            self.click("Full_recompute")
            self.page.wait_for_timeout(5000)
            self.wait_for_load_state("networkidle")
            self.switch_to_new_tab()
            self.close_new_tab_and_switch_back()
            log1.logger.info("Taxpayer details entered and compute completed")
            return self

