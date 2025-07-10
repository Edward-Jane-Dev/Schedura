import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestBasic(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_basic(self):
        self.driver.get("http://localhost:8000/")
        self.assertIn("Schedura", self.driver.page_source)
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()