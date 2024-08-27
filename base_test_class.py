import unittest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os

class BaseTestCase(unittest.TestCase):

    def tearDown(self, driver: webdriver.Chrome):
        """Capture screenshot and HTML content if the test fails."""

        test_exceptions = self._outcome.result.errors
        test_failures = self._outcome.result.failures
        if any(error for (_, error) in test_exceptions) or test_failures:
            self.capture_debug_info(driver)

        super().tearDown()
        # driver.quit()


    def capture_debug_info(self, driver: webdriver.Chrome):
        """Capture screenshots and HTML content for debugging."""

        try:
            if not os.path.exists('debug'):
                os.makedirs('debug')
            screenshot_path = os.path.join('debug', f"{self.id()}_screenshot.png")
            html_path = os.path.join('debug', f"{self.id()}_page.html")

            # Capture screenshot
            driver.save_screenshot(screenshot_path)
            
            # Capture HTML content
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)

        except WebDriverException as e:
            print(f"Failed to capture screenshot or HTML: {e}")
