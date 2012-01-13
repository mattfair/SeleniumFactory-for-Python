from selenium import webdriver
import unittest, time, re
import os
import json

from ParseSauceURL import *
from SeleniumFactory import *

"""
"""
class testSauceWrappers(unittest.TestCase):
    username = "rossco_9_9"
    access_key = "blah-blah-blah"
    def setUp(self):
        self.url = "sauce-ondemand:?username=%s&access-key=%s&job-name=simple test&os=Linux&browser=firefox&browser-version=7&firefox-profile-url=&idle-timeout=90&user-extensions-url=" % (self.username, self.access_key)
        os.environ["SELENIUM_DRIVER"] = self.url
        os.environ["SELENIUM_PORT"] = "80"
        os.environ["SELENIUM_HOST"] = "ondemand.saucelabs.com"
        os.environ["SELENIUM_STARTING_URL"]= "http://www.amazon.com"

    def retrieve_job_details(self, browser):
        sauceRest = SauceRest(self.username, self.access_key)
        result = sauceRest.get(browser.id())
        data = json.loads(result)
        return data

    def test_webdriver_success(self):

        browser = SeleniumFactory().createWebDriver()
        browser.get("http://amazon.com")
        assert "Amazon.com" in browser.title
        browser.job_passed()
        data = self.retrieve_job_details(browser)
        assert data['passed']
        browser.quit()

    def test_webdriver_failed(self):

        browser = SeleniumFactory().createWebDriver()
        browser.get("http://amazon.com")
        assert "Amazon.com" in browser.title
        browser.job_failed()
        data = self.retrieve_job_details(browser)
        assert not data['passed']
        browser.quit()

    def test_selenium_success(self):
        browser = SeleniumFactory().create()
        browser.open("http://www.amazon.com")
        assert "Amazon.com" in browser.get_title()
        browser.job_passed()
        data = self.retrieve_job_details(browser)
        assert data['passed']
        browser.stop()

    def test_selenium_failed(self):
        browser = SeleniumFactory().create()
        browser.open("http://www.amazon.com")
        assert "Amazon.com" in browser.get_title()
        browser.job_failed()
        data = self.retrieve_job_details(browser)
        assert not data['passed']
        browser.stop()

if __name__ == "__main__":
    unittest.main()