import os
import allure

from pages.BasePage import BasePage
from pages.HomePage import CreateNewReturn
from testcases.BaseTest import BaseTest
from utilities import dataProvider
from utilities import excel_util

EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "exceldata", "ReturnDetails.xlsx")
SHEET_NAME = "ReturnDetails"


class TestCreateReturnTest(BaseTest):

    def test_createReturn(self, page):
        with allure.step("*******Executing Create Return Test********"):
            locator_col = excel_util.get_col_by_header(EXCEL_PATH, SHEET_NAME, "Locator")
            for row_num, row in enumerate(dataProvider.get_data(SHEET_NAME, "ReturnDetails.xlsx"), start=2):
                Year, Type, Fname, Lname, SSN, DOB, Address1, Address2, Apartment, City, County, State, Zip, *_ = row
                enter_page = CreateNewReturn(page)\
                .select_createReturn()\
                .create_new_Return()\
                .Fill_details(str(Year), str(Type), str(Fname), str(Lname))\
                .Select_Mode()\
                .EnterDetails(str(SSN), str(DOB), str(Address1), str(Address2), str(Apartment), str(City), str(County), str(State), str(Zip))
                assert enter_page.captured_locator_id, \
                    f"Row {row_num}: Locator ID was not captured for {Fname} {Lname} — EnterDetails may have failed"
                excel_util.set_cell_data(EXCEL_PATH, SHEET_NAME, row_num, locator_col, enter_page.captured_locator_id)
            BasePage(page).logout()