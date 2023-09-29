import time
import logging

import requests

max_retries = 3  # Maximum number of retry attempts
retry_delay_seconds = 5  # Delay between retries in seconds

url1 = 'http://127.0.0.1:5003/stop_server'
url2 = 'http://127.0.0.1:5001/stop_server'


def make_request_with_retry(url):
    logging.info(f"Stopping Server url: {url} .")

    for retry_attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            logging.info(f"Server at {url} responded with status code 200.")
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while stopping server at {url}: {e}")
            if retry_attempt < max_retries - 1:
                logging.debug(f"Retrying in {retry_delay_seconds} seconds...")
                time.sleep(retry_delay_seconds)
            else:
                logging.warning(f"Max retries reached for {url}. Exiting.")


# Usage
response1 = make_request_with_retry(url1)
response2 = make_request_with_retry(url2)
