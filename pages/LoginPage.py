import logging

from pages.BasePage import BasePage
from pages.HomePage import CreateNewReturn
from utilities.generate_log import Logger

log = Logger(__name__, logging.DEBUG)


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def do_login(self, LoginID, Firm, Location, Password):
        try:
            log.logger.info(f"Logging in with LoginID: {LoginID}, Firm: {Firm}, Location: {Location}")
            self.type("LoginID_CSS", LoginID)
            self.type("Firm_CSS", Firm)
            self.type("Location_CSS", Location)
            self.type("Password_CSS", Password)
            self.click("login_CSS")
            self.wait_for_load_state("networkidle")
            log.logger.info("Login successful, navigating to Home page")
            return CreateNewReturn(self.page)
        except Exception as e:
            log.logger.error(f"Login failed for LoginID: {LoginID}, Firm: {Firm}, Location: {Location}. Error: {e}")
            raise
        finally:
            log.logger.info("Login attempt completed")





