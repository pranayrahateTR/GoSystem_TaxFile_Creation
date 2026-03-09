import allure
import pytest

from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestLoginTest(BaseTest):
    @pytest.mark.dependency(name="login")
    @pytest.mark.parametrize(("LoginID", "Firm", "Location", "Password"), dataProvider.get_data("Sheet1"))

    def test_login(self, page, LoginID, Firm, Location, Password):
        with allure.step("*******Executing Login Test********"):
            returns_page = LoginPage(page)\
                .do_login(LoginID, Firm, Location, Password)\
                .select_createReturn()
            returns_page.verify_element_visible("create_return_btn")







