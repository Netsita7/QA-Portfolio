import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TestAliExpressAddToCart(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.aliexpress.com")
        self.wait = WebDriverWait(self.driver, 10)
        
        # Create screenshot directory
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
    
    def test_add_single_item(self):
        """Test adding a single item to cart"""
        try:
            # Close popup if present
            try:
                close_btn = self.driver.find_element(By.CLASS_NAME, "next-dialog-close")
                close_btn.click()
            except:
                pass
            
            # Search for product
            search_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "search-key"))
            )
            search_box.send_keys("wireless headphones")
            search_box.submit()
            
            # Click first product
            first_product = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".item .list-item"))
            )
            first_product.click()
            
            # Switch to new tab
            self.driver.switch_to.window(self.driver.window_handles[1])
            
            # Add to cart
            add_to_cart_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-btn"))
            )
            add_to_cart_btn.click()
            
            # Verify success message
            success_msg = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-message"))
            )
            
            # Take screenshot
            self.driver.save_screenshot("screenshots/success_add_to_cart.png")
            
            print("✓ Test passed: Item added to cart successfully")
            
        except Exception as e:
            self.driver.save_screenshot("screenshots/test_failed.png")
            raise e
    
    def tearDown(self):
        """Cleanup after each test"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
