import unittest
from unittest import TestCase
import logging
import pymysql
import pytest
import requests

from db_connector import connect_to_database, close_connection, setup_database, \
    get_app_configuration_from_db, populate_config_table


# Post a new user data to the REST API using POST method.
# Submit a GET request to make sure status code is 200 and data equals to the
# posted data.
# Check posted data was stored inside DB (users table).
class IntegrationTests(TestCase):

    # global variables
    api_url = None
    user_name = None
    url_link_data = None
    last_added_user_id = None

    @classmethod
    def setUpClass(cls):
        logging.info("Setting up database tables at class level...")
        setup_database()
        populate_config_table()

        logging.info("Retrieving data from config table at class level...")

        cls.url_link_data = get_app_configuration_from_db()
        cls.api_url = None
        cls.user_name = None
        cls.post_data = None
        cls.last_added_user_id = None

        if cls.url_link_data:
            cls.user_name = cls.url_link_data[0]
            cls.api_url = cls.url_link_data[1]
            cls.post_data = {"user_name": cls.user_name}

    def test_step_1_post_john_status_200(self):
        logging.info("Test creation of user john with POST")

        post_response = requests.post(self.api_url, json={"user_name": self.user_name})
        pytest.last_added_user_id = post_response.json().get("added_user_id")
        assert post_response.status_code == 200

    def test_step_2_get_john_status_200(self):
        print(" Test retrieving of user john with GET")

        get_response = requests.get(self.api_url + str(pytest.last_added_user_id))
        self.assertEqual(get_response.status_code, 200)

        extract_user_name = get_response.json().get("user_name")
        self.assertEqual(extract_user_name, self.user_name, f"Unexpected JSON content: {extract_user_name}")

        # Assert the actual JSON content matches the expected JSON content
        assert extract_user_name == self.user_name, f"Unexpected JSON content: {extract_user_name}"


if __name__ == "__main__":
    unittest.main()
