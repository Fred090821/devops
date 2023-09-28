import time
import unittest
from unittest import TestCase

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from db_connector import get_next_available_row_id_from_db

driver = webdriver.Chrome()


# Start a Selenium Webdriver session.
# Navigate to web interface URL using an existing user id.
# Check that the user's name element is showing (web element exists).
# Print user name (using locator).
class FrontEndTest(TestCase):
    def test_John_using_selenium(self):
        print(" Test creation of user John using SELENIUM")

        # since the utility get_next_available_row_id_from_db generate the next available
        # id, we need the id currently so => get_next_available_row_id_from_db() - 1
        self.user_Id = get_next_available_row_id_from_db() - 1

        url_to_test = "http://127.0.0.1:5001/users/get_user_data/" + str(self.user_Id)
        try:
            driver.get(url_to_test)
            print("Current URL:", driver.current_url)

            try:
                username = driver.find_element(By.ID, "user")
                print("User Name:", username.text)
            except NoSuchElementException:
                print("User name element not found.")

            time.sleep(15)  # Waiting for demonstration purposes

        finally:
            driver.quit()


if __name__ == '__main__':
    unittest.main()
