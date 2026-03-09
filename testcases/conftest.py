import allure
import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

from utilities import configReader
from utilities import dataProvider

def take_screenshot(page, screenshot_name="screenshot", subfolder="screenshots"):
    """
    Reusable function to take screenshots with timestamp

    Args:
        page: Playwright page object
        screenshot_name: Base name for the screenshot (default: "screenshot")
        subfolder: Folder name to store screenshots (default: "screenshots")

    Returns:
        str: Path where screenshot was saved
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create screenshot directory path
    screenshot_dir = os.path.join(os.getcwd(), subfolder)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Create full file path with timestamp
    screenshot_path = os.path.join(screenshot_dir, f"{screenshot_name}_{timestamp}.png")

    # Take screenshot
    page.screenshot(path=screenshot_path, full_page=True)

    print(f"Screenshot saved: {screenshot_path}")
    return screenshot_path


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_instance=p.chromium.launch(headless=False,slow_mo=1000,args=["--start-maximized"])
        yield browser_instance
        browser_instance.close()

@pytest.fixture(scope="session",autouse=True)
def setup_function(page):
    page.goto(configReader.readConfig("basic info","testsiteurl"), wait_until="domcontentloaded") #Reading URL from Contest.py file
    page.wait_for_load_state("networkidle")  # Wait for page to be fully loaded

@pytest.fixture(scope="session")
def page(browser):
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    yield page
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to make test result available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
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