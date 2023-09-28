import logging
import os
import platform
import signal

import pymysql
from flask import Flask, jsonify, request

from db_connector import connect_to_database, close_connection

app = Flask(__name__)

# Configure logging formatting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


# A simple method route API for web app
# combining the default path and a given user id, the GET method
# retrieves the associated user's name to populate a placeholder
# in the returned HTML template or return no such user error
@app.route('/users/get_user_data/<user_id>', methods=['GET'])
def get_user_id(user_id):
    if request.method == 'GET':
        log.debug("Entered GET method call")
        conn = None
        cursor = None

        try:
            # Connect to the database
            conn = connect_to_database()
            if not conn:
                return jsonify({"status": "error", "reason": "Database connection error."}), 500

            log.debug("Connected to the database...")
            cursor = conn.cursor()

            log.debug(f"Executing query with user_id = {user_id}")

            cursor.execute(f"SELECT user_name FROM users WHERE user_id = %s", user_id)
            result = cursor.fetchone()

            if result:
                log.debug(f"Returning result with user_id = {user_id}")
                return f"<h1 id='user'> {result[0]} </h1>"
            else:
                log.warning(f"Returning result with user_id = {user_id}")
                return f"<h1 id='error'> no such user: {user_id}</h1>"

        except pymysql.MySQLError as query_error:
            log.error(f"Query execution error: {query_error}")
            return jsonify({"status": "error", "reason": "Database error."}), 500

        except Exception as exception:
            log.error(f"An error occurred: {exception}")
            return jsonify({"status": "error", "reason": "An error occurred."}), 500

        finally:
            close_connection(conn, cursor)


# route to stop the server during jenkins pipeline run
# avoiding perpetual run
@app.route('/stop_server')
def shutdown():
    print("Shutting down gracefully...")
    operating_system = platform.system()
    if operating_system == "Windows":
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
    else:
        os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)
