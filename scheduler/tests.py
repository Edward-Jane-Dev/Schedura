from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Create your tests here.

class HomePageSeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        cls.browser = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_homepage_button_redirects_to_schedule(self):
        self.browser.get(self.live_server_url + '/')
        button = self.browser.find_element(By.LINK_TEXT, 'Go to Schedule')
        button.click()
        time.sleep(1)  # Wait for navigation
        self.assertIn('/schedule/', self.browser.current_url)
