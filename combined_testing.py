import logging
import time
import unittest
from unittest import TestCase

import pymysql
import pytest
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from db_connector import connect_to_database, close_connection, setup_database, \
    get_app_configuration_from_db, populate_config_table, delete_all_rows


# Post any new user data to the REST API using POST method.
# Submit a GET request to make sure data equals to the posted data.
# Using pymysql, check posted data was stored inside DB (users table).
# Start a Selenium Webdriver session.
# Navigate to web interface URL using the new user id.
# Check that the user's name is correct.
# Any failure will throw an exception using the following code: raise Exception("test failed")
class IntegrationTest(TestCase):
    # global variables
    api_url = None
    user_name = None
    url_link_data = None
    last_added_user_id = None
    browser = None

    @classmethod
    def setUpClass(cls):
        print("Setting up database tables at class level...")
        setup_database()
        populate_config_table()

        print("Retrieving data from config table at class level...")

        cls.url_link_data = get_app_configuration_from_db()
        cls.api_url = None
        cls.user_name = None
        cls.post_data = None
        cls.last_added_user_id = None
        cls.browser = None

        if cls.url_link_data:
            cls.user_name = cls.url_link_data[0]
            cls.api_url = cls.url_link_data[1]
            cls.post_data = {"user_name": cls.user_name}

    def test_post_john_status_200(self):
        print("Test creation of user john with POST")

        post_response = requests.post(self.api_url, json={"user_name": self.user_name})
        pytest.last_added_user_id = post_response.json().get("added_user_id")
        assert post_response.status_code == 200

    def test_step_2_get_user_name_john_status_200(self):
        print(" Test retrieving of user john with GET")

        get_response = requests.get(self.api_url + str(pytest.last_added_user_id))
        self.assertEqual(get_response.status_code, 200)

        extract_user_name = get_response.json().get("user_name")
        self.assertEqual(extract_user_name, self.user_name, f"Unexpected JSON content: {extract_user_name}")

        # Assert the actual JSON content matches the expected JSON content
        assert extract_user_name == self.user_name, f"Unexpected JSON content: {extract_user_name}"

    def test_step_3__database_verification_for_john_created_200(self):
        print(" Test database for creation of user john using parametrized query")

        conn = None
        cursor = None
        try:
            # Connect to the database
            conn = connect_to_database()
            if not conn:
                return "Database connection error."

            cursor = conn.cursor()

            try:
                select_query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
                cursor.execute(select_query, str(pytest.last_added_user_id, ))
                result = cursor.fetchone()
                if result:
                    print(self.user_name + " = " + str(result[1]))
                    assert result[1] == self.user_name
                else:
                    assert False, "condition not met"

            except pymysql.MySQLError as query_error:
                print(f"Query execution error: {query_error}")

        finally:
            print("close all connections")
            # Close the connection and cursor
            close_connection(conn, cursor)

    def test_step_4_get_user_name_john_status_200_using_selenium(self):
        print(" Test creation of user john using SELENIUM")

        if pytest.last_added_user_id is not None:
            url_selenium = self.api_url + str(pytest.last_added_user_id)

            if self.browser == "Chrome":
                driver = webdriver.Chrome()

                print(f"BROWSER : %S", self.browser)
                try:
                    driver.get(url_selenium)

                    # Check that the user_name element is showing (web element exists)
                    try:
                        username = driver.find_element(By.ID, "user")
                    except NoSuchElementException:
                        time.sleep(15)

                finally:
                    driver.quit()

        else:
            assert False, "condition not met"

    # @classmethod
    # def tearDownClass(cls):
    #     print(" Clear test context at class level")
    #     delete_all_rows('users')
    #     delete_all_rows('config')


if __name__ == "__main__":
    unittest.main()
