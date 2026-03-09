# GoSystem Test Automation — Before & After Changes

**Date:** 2026-03-04
**Scope:** Fix sequential execution of `LoginTest.py` → `CreateReturnTest.py`
**Files Modified:** 6

---

## Table of Contents
1. [testcases/LoginTest.py](#1-testcaseslogintestpy)
2. [testcases/CreateReturnTest.py](#2-testcasescreatereturn testpy)
3. [testcases/conftest.py](#3-testcasesconftestpy)
4. [pages/LoginPage.py](#4-pagesloginpagepy)
5. [pages/ReturnsPage.py](#5-pagesreturnspagepy)
6. [pages/EnterDetailsPage.py](#6-pagesenterdetailspagepy)

---

## 1. `testcases/LoginTest.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Bug 4 | `Year, Type, Fname, Lname` in function signature had no data source — pytest failed to collect the test | CRITICAL |
| Issue 9 | No assertion after login — test always "passed" even on failure | Medium |

### BEFORE
```python
import allure
import pytest

from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestLoginTest(BaseTest):

    @pytest.mark.parametrize(("LoginID", "Firm", "Location", "Password"), dataProvider.get_data("Sheet1"))

    def test_login(self, page, LoginID,Firm, Location, Password,Year,Type,Fname,Lname):
        with allure.step("*******Executing Login Test********"):


            # lp=LoginPage(page)
            # #Wwhen user is using pytest fixtures instead of dataprovider and if more than 1 argument is present then user need to add **fixture name
            # lp.do_login(LoginID,Firm, Location, Password)
            # time.sleep(3)
            # hp=CreateNewReturn(page).select_createReturn(page).create_new_Return(page).Fill_details(Year,Type,Fname,Lname)
            # time.sleep(30000)
            #

            LoginPage(page)\
            .do_login(LoginID,Firm, Location, Password)\
            .select_createReturn()
```

### AFTER
```python
import allure
import pytest

from pages.LoginPage import LoginPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestLoginTest(BaseTest):

    @pytest.mark.parametrize(("LoginID", "Firm", "Location", "Password"), dataProvider.get_data("Sheet1"))

    def test_login(self, page, LoginID, Firm, Location, Password):
        with allure.step("*******Executing Login Test********"):
            returns_page = LoginPage(page)\
                .do_login(LoginID, Firm, Location, Password)\
                .select_createReturn()
            returns_page.verify_element_visible("create_return_btn")
```

### What Changed
- Removed `Year, Type, Fname, Lname` from the method signature — they were not present in `@pytest.mark.parametrize` and are not fixtures, causing pytest collection to fail with `fixture 'Year' not found`.
- Captured the return value of `.select_createReturn()` into `returns_page`.
- Added `returns_page.verify_element_visible("create_return_btn")` as a meaningful assertion to confirm the user successfully landed on the Returns page post-login.
- Removed all dead commented-out code.

---

## 2. `testcases/CreateReturnTest.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Issue 10 | Class named `test_createReturnTest` — non-standard pytest convention (lowercase `t`) | Low |
| Bug 2 | `ReturnsPage(self)` passed the test class instance instead of the Playwright `page` object | CRITICAL |
| Bug 3 | `.EnterDetailsPage()` method does not exist on `ReturnsPage` — caused `AttributeError` | CRITICAL |
| Bug 1 (indirect) | Test had no login step; `setup_function` resets browser to login URL before every test, so the test always started unauthenticated | CRITICAL |

### BEFORE
```python
import allure
import pytest

from pages.ReturnsPage import ReturnsPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class test_createReturnTest(BaseTest):

    @pytest.mark.parametrize(("Year","Type","Fname","Lname"),dataProvider.get_data("createreturn"))

    def test_createReturn(self, page,Year,Type,Fname,Lname):
        with allure.step("*******Executing Create Return Test********"):
            ReturnsPage(self)\
            .create_new_Return()\
            .Fill_details(Year,Type,Fname,Lname)\
            .EnterDetailsPage()\
            .logout()
```

### AFTER
```python
import allure
import pytest

from pages.LoginPage import LoginPage
from pages.ReturnsPage import ReturnsPage
from testcases.BaseTest import BaseTest
from utilities import dataProvider


class TestCreateReturnTest(BaseTest):

    @pytest.mark.parametrize(("Year","Type","Fname","Lname"),dataProvider.get_data("createreturn"))

    def test_createReturn(self, page, login_credentials, Year, Type, Fname, Lname):
        with allure.step("*******Executing Create Return Test********"):
            LoginID, Firm, Location, Password = login_credentials
            LoginPage(page)\
            .do_login(LoginID, Firm, Location, Password)\
            .select_createReturn()\
            .create_new_Return()\
            .Fill_details(Year, Type, Fname, Lname)\
            .Select_Mode()\
            .EnterDetails()\
            .logout()
```

### What Changed
- **Class renamed** `test_createReturnTest` → `TestCreateReturnTest` to follow standard pytest class naming convention.
- **Added import** `from pages.LoginPage import LoginPage` — required for the login step.
- **Added `login_credentials` fixture parameter** — reads credentials from Sheet1[0] in Excel (provided by `conftest.py`), making the test self-contained without modifying the Excel file.
- **Replaced `ReturnsPage(self)`** with a full method chain starting from `LoginPage(page).do_login(...)` — test now correctly starts from the login page (which `setup_function` always navigates to) and handles its own authentication.
- **Fixed method chain**: replaced `.EnterDetailsPage()` (non-existent method) with `.Select_Mode().EnterDetails()` — `Select_Mode()` handles the user mode popup and returns an `EnterDetailsPage` object; `EnterDetails()` fills in taxpayer data.

---

## 3. `testcases/conftest.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Issue 6 | `capture_screenshot_on_failure` was `session`-scoped — `request.node` at session scope is the session object, not the test item, so `rep_call` is never set and screenshots are never captured on failure | High |
| New fixture | `login_credentials` fixture needed by `CreateReturnTest` to get login data without touching Excel structure | — |

### BEFORE (relevant sections)
```python
from utilities import configReader

# ...

@pytest.fixture(scope="session")
def capture_screenshot_on_failure(request, page):
    yield
    item = request.node
    # Check if the test failed
    if hasattr(item, "rep_call") and item.rep_call.failed:
        try:
            # Create screenshot directory if it doesn't exist
            os.makedirs("screenshot", exist_ok=True)
            screenshot_data = page.screenshot(path="screenshot/fullpage.png")
            allure.attach(screenshot_data, name="failurescreenshot",
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Could not capture screenshot: {e}")

# @pytest.fixture
# def use_creds():
#     return {"LoginID":"PRAHATE","Firm":"600M", "Location":"MUMBAI", "Password":"Scrambler@400T"}
```

### AFTER (relevant sections)
```python
from utilities import configReader
from utilities import dataProvider

# ...

@pytest.fixture(scope="function")          # <-- was scope="session"
def capture_screenshot_on_failure(request, page):
    yield
    item = request.node
    # Check if the test failed
    if hasattr(item, "rep_call") and item.rep_call.failed:
        try:
            # Create screenshot directory if it doesn't exist
            os.makedirs("screenshot", exist_ok=True)
            screenshot_data = page.screenshot(path="screenshot/fullpage.png")
            allure.attach(screenshot_data, name="failurescreenshot",
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Could not capture screenshot: {e}")


@pytest.fixture
def login_credentials():
    """Returns (LoginID, Firm, Location, Password) from the first row of Sheet1."""
    creds = dataProvider.get_data("Sheet1")
    return tuple(creds[0])
```

### What Changed
- **Added import** `from utilities import dataProvider` at the top.
- **`capture_screenshot_on_failure` scope** changed from `"session"` to `"function"`. At session scope, `request.node` points to the session object — it never has `rep_call` set per test. At function scope it correctly points to the individual test item, enabling per-test failure screenshots.
- **Added `login_credentials` fixture** — reads the first row from the `Sheet1` sheet of `testdata.xlsx` and returns credentials as a tuple `(LoginID, Firm, Location, Password)`. This is consumed by `CreateReturnTest.py` so it can log in without requiring its own parametrize for credentials.

---

## 4. `pages/LoginPage.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Issue 7 | `time.sleep(10)` hardcoded wait after login click — unreliable and slow | High |
| Cleanup | Unused imports: `time`, `sync_playwright`, `pytest`, `configReader` | Low |

### BEFORE
```python
import time

from playwright.sync_api import sync_playwright
import pytest

from pages.BasePage import BasePage
from pages.HomePage import CreateNewReturn
from utilities import configReader


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def do_login(self,LoginID,Firm,Location,Password):
        self.type("LoginID_CSS", LoginID)
        self.type("Firm_CSS", Firm)
        self.type("Location_CSS", Location)
        self.type("Password_CSS", Password)
        self.click("login_CSS")
        time.sleep(10)
        return CreateNewReturn(self.page)
```

### AFTER
```python
from pages.BasePage import BasePage
from pages.HomePage import CreateNewReturn


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def do_login(self, LoginID, Firm, Location, Password):
        self.type("LoginID_CSS", LoginID)
        self.type("Firm_CSS", Firm)
        self.type("Location_CSS", Location)
        self.type("Password_CSS", Password)
        self.click("login_CSS")
        self.wait_for_load_state("networkidle")
        return CreateNewReturn(self.page)
```

### What Changed
- **Removed unused imports**: `time`, `sync_playwright`, `pytest`, `configReader` — none of these were used in this file.
- **Replaced `time.sleep(10)`** with `self.wait_for_load_state("networkidle")` — waits until all network requests settle after login, then proceeds. This is faster when the page loads quickly and more reliable when it takes longer than 10 seconds.

---

## 5. `pages/ReturnsPage.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Issue 7 | 5 × `time.sleep()` calls totalling up to 19 seconds of fixed delay | High |
| Cleanup | Unused import: `time` | Low |

### BEFORE
```python
import time

import allure
from playwright.sync_api import expect

from pages.BasePage import BasePage
from pages.EnterDetailsPage import EnterDetailsPage


class ReturnsPage(BasePage):
    def __init__(self,page):
        super().__init__(page)

#_________________________Create New Returns___________________________#
    def create_new_Return(self):
        self.click("create_return_btn")
        return self

    def Fill_details(self,Year,Type,Fname,Lname):
        with allure.step(f"Filling details for Taxpayer"):
# select Tax Year
            self.type("select_year",str(Year))
            time.sleep(3)
    # select return Type
            self.type("Select Type",str(Type))
            time.sleep(2)
    #Enter Taxpayer info
            self.type("fname_css",Fname)
            time.sleep(2)
            self.type("lname_css",Lname)
            time.sleep(2)
            self.click("checkbox_css")
            time.sleep(2)
            self.click("create_btn")
            time.sleep(10)

            return self
#__________________Select Mode________________#
    def Select_Mode(self):
        with allure.step("Selecting  user mode from popup"):
            self.click("single_user")
            self.click_and_switch_to_new_tab("continue_btn")
            time.sleep(2)
            return EnterDetailsPage(self.page)
```

### AFTER
```python
import allure
from playwright.sync_api import expect

from pages.BasePage import BasePage
from pages.EnterDetailsPage import EnterDetailsPage


class ReturnsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

#_________________________Create New Returns___________________________#
    def create_new_Return(self):
        self.click("create_return_btn")
        return self

    def Fill_details(self, Year, Type, Fname, Lname):
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
            self.click("create_btn")
            self.wait_for_load_state("networkidle")
            return self

#__________________Select Mode________________#
    def Select_Mode(self):
        with allure.step("Selecting user mode from popup"):
            self.click("single_user")
            self.click_and_switch_to_new_tab("continue_btn")
            self.wait_for_load_state("networkidle")
            return EnterDetailsPage(self.page)
```

### What Changed

| Location | Before | After | Reason |
|---|---|---|---|
| After `type("select_year",...)` | `time.sleep(3)` | `self.wait_for_load_state("domcontentloaded")` | Year field may trigger a dynamic update; wait for DOM to settle |
| After `type("Select Type",...)` | `time.sleep(2)` | _(removed)_ | Playwright auto-waits for element actionability before `fill()` |
| After `type("fname_css",...)` | `time.sleep(2)` | _(removed)_ | Same — auto-wait covers this |
| After `type("lname_css",...)` | `time.sleep(2)` | _(removed)_ | Same |
| After `click("checkbox_css")` | `time.sleep(2)` | _(removed)_ | Same |
| After `click("create_btn")` | `time.sleep(10)` | `self.wait_for_load_state("networkidle")` | Form submission triggers a page load; wait for network to settle |
| After `click_and_switch_to_new_tab` | `time.sleep(2)` | `self.wait_for_load_state("networkidle")` | New tab needs to fully load before actions can be taken |

- **Removed `import time`** — no longer used.

---

## 6. `pages/EnterDetailsPage.py`

### Issues Fixed
| # | Issue | Severity |
|---|---|---|
| Bug 5 | `from playwright.async_api import Page` — wrong API import in a sync project | Low |
| Issue 7 | 13 × `time.sleep()` calls totalling 18 seconds of fixed delay | High |
| Cleanup | Unused import: `time` | Low |

### BEFORE
```python
import time

from playwright.async_api import Page

from pages.BasePage import BasePage


class EnterDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def EnterDetails(self):
        self.click_by_text("general_info_txt")
        time.sleep(1)
        self.click_by_text("basic_return_info")
        time.sleep(1)
        self.click_by_text("Taxpayer_info")
        time.sleep(1)
        self.select_custom_dropdown("Filling_state","Single")
        time.sleep(1)
        self.type("SSN","111-11-1111")
        time.sleep(1)
        self.type("DOB","12/12/1995")
        time.sleep(1)

        #Address Details
        self.type("Address1","ABC")
        time.sleep(1)
        self.type("Address2","DEF")
        time.sleep(1)
        self.type("Apartment","232")
        time.sleep(1)
        self.type("city","SLC")
        time.sleep(1)
        self.type("county","DC")
        time.sleep(1)

        self.select_custom_dropdown("state","AL - Alabama")
        time.sleep(1)
        self.type("zip","12353")
        time.sleep(1)
        self.click("compute")
        time.sleep(1)
        self.click("Full_recompute")
        time.sleep(5)
        self.switch_to_new_tab()
        self.close_new_tab_and_switch_back()
        return self
```

### AFTER
```python
from playwright.sync_api import Page

from pages.BasePage import BasePage


class EnterDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def EnterDetails(self):
        self.click_by_text("general_info_txt")
        self.click_by_text("basic_return_info")
        self.click_by_text("Taxpayer_info")
        self.select_custom_dropdown("Filling_state", "Single")
        self.type("SSN", "111-11-1111")
        self.type("DOB", "12/12/1995")

        # Address Details
        self.type("Address1", "ABC")
        self.type("Address2", "DEF")
        self.type("Apartment", "232")
        self.type("city", "SLC")
        self.type("county", "DC")
        self.select_custom_dropdown("state", "AL - Alabama")
        self.type("zip", "12353")
        self.click("compute")
        self.click("Full_recompute")
        self.wait_for_load_state("networkidle")
        self.switch_to_new_tab()
        self.close_new_tab_and_switch_back()
        return self
```

### What Changed

| Location | Before | After | Reason |
|---|---|---|---|
| Import | `from playwright.async_api import Page` | `from playwright.sync_api import Page` | Project uses sync Playwright; async import was incorrect |
| Between navigation clicks (×3) | `time.sleep(1)` each | _(removed)_ | `click_by_text()` in BasePage uses Playwright's built-in auto-wait |
| Between field inputs (×10) | `time.sleep(1)` each | _(removed)_ | `type()` and `select_custom_dropdown()` auto-wait for element to be actionable |
| Before `switch_to_new_tab()` | `time.sleep(5)` | `self.wait_for_load_state("networkidle")` | Full recompute triggers network activity; wait for it to finish before switching |

- **Removed `import time`** — no longer used.
- **Removed `import time`** — 13 total `time.sleep()` calls removed, saving a minimum of 18 seconds per test run.

---

## Summary of All Changes

| File | Bugs Fixed | Issues Fixed | Lines Removed | Lines Added |
|---|---|---|---|---|
| `testcases/LoginTest.py` | Bug 4 | Issue 9 | 13 | 4 |
| `testcases/CreateReturnTest.py` | Bug 1, Bug 2, Bug 3 | Issue 10 | 4 | 8 |
| `testcases/conftest.py` | — | Issue 6 | 2 | 8 |
| `pages/LoginPage.py` | — | Issue 7 | 6 | 1 |
| `pages/ReturnsPage.py` | — | Issue 7 | 6 | 3 |
| `pages/EnterDetailsPage.py` | Bug 5 | Issue 7 | 15 | 2 |

### Time Saved Per Test Run (Issue 7)

| File | Sleep Removed |
|---|---|
| `LoginPage.py` | 10 seconds |
| `ReturnsPage.py` | Up to 19 seconds |
| `EnterDetailsPage.py` | 18 seconds |
| **Total per test** | **~47 seconds** |

For a parametrized suite with N rows in `createreturn` sheet, the saving is **N × ~47 seconds**.

---

## How to Run After These Fixes

```bash
# Run LoginTest only
pytest testcases/LoginTest.py -v

# Run CreateReturnTest only
pytest testcases/CreateReturnTest.py -v

# Run both sequentially (original requirement)
pytest testcases/LoginTest.py testcases/CreateReturnTest.py -v

# Run with Allure report generation
pytest testcases/LoginTest.py testcases/Crea teReturnTest.py -v --alluredir=allure-results
allure serve allure-results
```
