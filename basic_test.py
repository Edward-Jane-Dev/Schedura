import unittest
from selenium import webdriver

class TestBasic(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_basic(self):
        self.driver.get("http://localhost:8000/")
        self.assertIn("Congratulations!", self.driver.title)
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()