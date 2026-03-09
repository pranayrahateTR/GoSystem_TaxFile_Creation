import logging

import allure
from playwright.sync_api import expect

from utilities import configReader
from utilities.generate_log import Logger

log=Logger(__name__,logging.DEBUG)

class BasePage:

    def __init__(self, page):
        self.page = page

    def click(self,locator):
        with allure.step(f"Clicking on an element{locator}"):
         self.page.locator(configReader.readConfig("locators",locator)).click()
        log.logger.info(f"Clicking on a button {locator}")

    def type(self,locator,value):
        with allure.step(f"Typing in an Element {locator} and entered value as {value}"):
         self.page.locator(configReader.readConfig("locators",locator)).fill(value)
        log.logger.info(f"Typing in an Element {locator} and entered value as {value}")

    def move_to(self,locator):
        with allure.step(f"Moving to an Element {locator}"):
            self.page.locator(configReader.readConfig("locators",locator)).hover()
        log.logger.info(f"Moving on a Element {locator}")

    def click_by_text(self, locator, exact=True, timeout=10):
        """Click element by visible text. Locator should contain the text value in conf.ini"""
        text = configReader.readConfig("locators", locator)
        with allure.step(f"clicking on element with text: {text}"):
            self.page.get_by_text(text, exact=exact).click(timeout=timeout * 1000)
            log.logger.info(f"clicked on element with text: {text}")

    def verify_text(self,locator,expected_key_text,timeout):
            locator=configReader.readConfig("locators",locator)
            expected_text=configReader.readConfig("locators",expected_key_text)
            with allure.step(f"Verifying element text {locator}"):

                expect(self.page.locator(locator).to_have_text(expected_text,timeout=timeout*1000))

                log.logger.info(f"Verifying element  {locator}: has text : {expected_text}")

    def get_text(self, locator):
        """Get text content from an element"""
        with allure.step(f"Getting text from element {locator}"):
            text = self.page.locator(configReader.readConfig("locators", locator)).inner_text()
            log.logger.info(f"Got text from element {locator}: {text}")
            return text

    def get_attribute(self, locator, attribute):
        """Get attribute value from an element"""
        with allure.step(f"Getting attribute '{attribute}' from element {locator}"):
            value = self.page.locator(configReader.readConfig("locators", locator)).get_attribute(attribute)
            log.logger.info(f"Got attribute '{attribute}' from element {locator}: {value}")
            return value

    def is_visible(self, locator, timeout=5000):
        """Check if element is visible"""
        try:
            with allure.step(f"Checking visibility of element {locator}"):
                visible = self.page.locator(configReader.readConfig("locators", locator)).is_visible(timeout=timeout)
                log.logger.info(f"Element {locator} visibility: {visible}")
                return visible
        except Exception as e:
            log.logger.warning(f"Element {locator} not visible: {str(e)}")
            return False

    def is_enabled(self, locator):
        """Check if element is enabled"""
        with allure.step(f"Checking if element {locator} is enabled"):
            enabled = self.page.locator(configReader.readConfig("locators", locator)).is_enabled()
            log.logger.info(f"Element {locator} enabled: {enabled}")
            return enabled

    def is_checked(self, locator):
        """Check if checkbox/radio is checked"""
        with allure.step(f"Checking if element {locator} is checked"):
            checked = self.page.locator(configReader.readConfig("locators", locator)).is_checked()
            log.logger.info(f"Element {locator} checked: {checked}")
            return checked

    def wait_for_element(self, locator, state="visible", timeout=30000):
        """Wait for element to be in specified state (visible, hidden, attached, detached)"""
        with allure.step(f"Waiting for element {locator} to be {state}"):
            self.page.locator(configReader.readConfig("locators", locator)).wait_for(state=state, timeout=timeout)
            log.logger.info(f"Element {locator} is now {state}")

    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        with allure.step(f"Selecting dropdown {locator} with value {value}"):
            self.page.locator(configReader.readConfig("locators", locator)).select_option(value=value)
            log.logger.info(f"Selected dropdown {locator} with value: {value}")

    def select_dropdown_by_label(self, locator, label):
        """Select dropdown option by visible label"""
        with allure.step(f"Selecting dropdown {locator} with label {label}"):
            self.page.locator(configReader.readConfig("locators", locator)).select_option(label=label)
            log.logger.info(f"Selected dropdown {locator} with label: {label}")

    def select_custom_dropdown(self, locator, label):
        """Select option from a custom saf-select web component (not a native <select>).
        Clicks the combobox to open it, then clicks the matching option in the listbox."""
        with allure.step(f"Selecting custom dropdown {locator} with label {label}"):
            self.page.locator(configReader.readConfig("locators", locator)).click()
            self.page.get_by_role("option", name=label, exact=True).click()
            log.logger.info(f"Selected custom dropdown {locator} with label: {label}")

    def check_checkbox(self, locator):
        """Check a checkbox"""
        with allure.step(f"Checking checkbox {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).check()
            log.logger.info(f"Checked checkbox {locator}")

    def uncheck_checkbox(self, locator):
        """Uncheck a checkbox"""
        with allure.step(f"Unchecking checkbox {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).uncheck()
            log.logger.info(f"Unchecked checkbox {locator}")

    def double_click(self, locator):
        """Double click on an element"""
        with allure.step(f"Double clicking on element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).dblclick()
            log.logger.info(f"Double clicked on element {locator}")

    def right_click(self, locator):
        """Right click (context click) on an element"""
        with allure.step(f"Right clicking on element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).click(button="right")
            log.logger.info(f"Right clicked on element {locator}")

    def clear_text(self, locator):
        """Clear text from input field"""
        with allure.step(f"Clearing text from element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).clear()
            log.logger.info(f"Cleared text from element {locator}")

    def field_is_editable(self,locator,timeout=30000):
        with allure.step(f"Checking if  {locator} is editable"):
            editable=self.page.locator(configReader.readConfig("locators",locator)).is_editable(timeout=timeout)
            log.logger.info(f"Checking if  {locator} is editable: {editable}")
            return editable

    def press_key(self, locator, key):
        """Press keyboard key on an element"""
        with allure.step(f"Pressing key '{key}' on element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).press(key)
            log.logger.info(f"Pressed key '{key}' on element {locator}")

    def upload_file(self, locator, file_path):
        """Upload file to input element"""
        with allure.step(f"Uploading file {file_path} to element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).set_input_files(file_path)
            log.logger.info(f"Uploaded file {file_path} to element {locator}")

    def get_page_title(self):
        """Get current page title"""
        with allure.step("Getting page title"):
            title = self.page.title()
            log.logger.info(f"Page title: {title}")
            return title

    def get_current_url(self):
        """Get current page URL"""
        with allure.step("Getting current URL"):
            url = self.page.url
            log.logger.info(f"Current URL: {url}")
            return url

    def navigate_to(self, url):
        """Navigate to a URL"""
        with allure.step(f"Navigating to {url}"):
            self.page.goto(url)
            log.logger.info(f"Navigated to {url}")

    def refresh_page(self):
        """Refresh the current page"""
        with allure.step("Refreshing page"):
            self.page.reload()
            log.logger.info("Page refreshed")

    def go_back(self):
        """Go back to previous page"""
        with allure.step("Going back"):
            self.page.go_back()
            log.logger.info("Navigated back")

    def go_forward(self):
        """Go forward to next page"""
        with allure.step("Going forward"):
            self.page.go_forward()
            log.logger.info("Navigated forward")

    def scroll_to_element(self, locator):
        """Scroll to an element"""
        with allure.step(f"Scrolling to element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).scroll_into_view_if_needed()
            log.logger.info(f"Scrolled to element {locator}")

    def get_element_count(self, locator):
        """Get count of elements matching locator"""
        with allure.step(f"Getting count of elements {locator}"):
            count = self.page.locator(configReader.readConfig("locators", locator)).count()
            log.logger.info(f"Element {locator} count: {count}")
            return count

    def verify_element_visible(self, locator, timeout=10000):
        """Verify element is visible"""
        with allure.step(f"Verifying element {locator} is visible"):
            expect(self.page.locator(configReader.readConfig("locators", locator))).to_be_visible(timeout=timeout)
            log.logger.info(f"Verified element {locator} is visible")

    def verify_element_hidden(self, locator, timeout=10000):
        """Verify element is hidden"""
        with allure.step(f"Verifying element {locator} is hidden"):
            expect(self.page.locator(configReader.readConfig("locators", locator))).to_be_hidden(timeout=timeout)
            log.logger.info(f"Verified element {locator} is hidden")

    def verify_url_contains(self, expected_url_part):
        """Verify current URL contains expected text"""
        with allure.step(f"Verifying URL contains '{expected_url_part}'"):
            expect(self.page).to_have_url(f".*{expected_url_part}.*")
            log.logger.info(f"Verified URL contains: {expected_url_part}")

    def verify_title_contains(self, expected_title):
        """Verify page title contains expected text"""
        with allure.step(f"Verifying title contains '{expected_title}'"):
            expect(self.page).to_have_title(f".*{expected_title}.*")
            log.logger.info(f"Verified title contains: {expected_title}")

    def take_screenshot(self, filename):
        """Take screenshot and save to file"""
        with allure.step(f"Taking screenshot: {filename}"):
            self.page.screenshot(path=filename)
            log.logger.info(f"Screenshot saved: {filename}")
            allure.attach.file(filename, attachment_type=allure.attachment_type.PNG)

    def execute_script(self, script, *args):
        """Execute JavaScript on the page"""
        with allure.step(f"Executing script: {script[:50]}..."):
            result = self.page.evaluate(script, *args)
            log.logger.info(f"Executed script: {script[:100]}")
            return result

    def click_with_force(self, locator):
        """Click element with force (bypasses actionability checks)"""
        with allure.step(f"Force clicking on element {locator}"):
            self.page.locator(configReader.readConfig("locators", locator)).click(force=True)
            log.logger.info(f"Force clicked on element {locator}")

    def type_slowly(self, locator, value, delay=100):
        """Type text slowly with delay between keystrokes"""
        with allure.step(f"Typing slowly in element {locator} with value {value}"):
            self.page.locator(configReader.readConfig("locators", locator)).type(value, delay=delay)
            log.logger.info(f"Typed slowly in element {locator}: {value}")

    def wait_for_load_state(self, state="load", timeout=30000):
        """Wait for page load state (load, domcontentloaded, networkidle)"""
        with allure.step(f"Waiting for page load state: {state}"):
            self.page.wait_for_load_state(state, timeout=timeout)
            log.logger.info(f"Page reached load state: {state}")

    def click_and_switch_to_new_tab(self, locator, timeout=30):
        """Click element that opens a new tab and switch context to it.
        timeout: seconds to wait for the new tab to open (default 30s).
        Stores the original page in self.original_page so you can close
        the new tab and return to it via close_new_tab_and_switch_back()."""
        with allure.step(f"Clicking {locator} and switching to new tab"):
            with self.page.context.expect_page(timeout=timeout * 1000) as new_page_info:
                self.click(locator)
            new_page = new_page_info.value
            new_page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            self.original_page = self.page
            self.page = new_page
            log.logger.info(f"Switched to new tab after clicking {locator}")
            return self

    def switch_to_new_tab(self):
        """Switch to a new tab only if one is already open.
        If no new tab exists, logs a warning and does nothing.
        Used when a tab MAY have been opened by a prior action (e.g. Full_recompute)."""
        with allure.step("Switching to new tab"):
            new_page = self.page.context.pages[-1]
            if new_page == self.page:
                log.logger.warning("No new tab detected — staying on current page")
                return self
            new_page.wait_for_load_state("networkidle")
            self.original_page = self.page
            self.page = new_page
            log.logger.info("Switched to new tab")
            return self

    def wait_for_new_tab_and_switch(self, timeout=30):
        """Wait for a new tab that opens automatically (no explicit click needed).
        First checks if a tab is already open; if not, waits up to timeout seconds.
        Used in Select_Mode() for 2nd+ returns where no popup appears.
        Stores original_page for close_new_tab_and_switch_back()."""
        with allure.step("Waiting for new tab and switching"):
            # Tab may have already opened during the prior networkidle wait
            new_page = self.page.context.pages[-1]
            if new_page != self.page:
                new_page.wait_for_load_state("networkidle", timeout=timeout * 1000)
                self.original_page = self.page
                self.page = new_page
                log.logger.info("Switched to new tab (already open)")
                return self
            # Tab not open yet — wait for it to appear
            with self.page.context.expect_page(timeout=timeout * 1000) as new_page_info:
                pass
            new_page = new_page_info.value
            new_page.wait_for_load_state("networkidle", timeout=timeout * 1000)
            self.original_page = self.page
            self.page = new_page
            log.logger.info("Switched to new tab (waited for it to open)")
            return self

    def close_new_tab_and_switch_back(self):
        """Close the current (new) tab and switch back to the original page.
        If switch_to_new_tab() was skipped (no new tab opened), does nothing."""
        with allure.step("Closing new tab and switching back to original page"):
            if not hasattr(self, "original_page") or self.original_page is None:
                log.logger.warning("No original page to switch back to — skipping close")
                return self
            self.page.close()
            self.page = self.original_page
            self.original_page = None
            log.logger.info("Closed new tab and switched back to original page")
            return self


    def logout(self):
        self.click("logout_CSS")
        log.logger.info("Logged Out")
        return self