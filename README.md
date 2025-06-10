# LunarLogger

LunarLogger is a powerful, Python-based keylogger designed for logging keystrokes, system information, clipboard data, audio recordings, and screenshots. The tool also provides secure encryption for logged data using the `cryptography.fernet` library to protect sensitive information before it's sent.

This project is intended for educational purposes only and should be used in controlled environments where you have explicit permission to monitor devices. Unauthorized use is illegal and unethical.

## Features
- **Keylogging:** Logs every keystroke made on the system.
- **System Information:** Captures essential details about the system, such as the processor, IP addresses, and more.
- **Clipboard Monitoring:** Captures clipboard contents (texts copied).
- **Audio Recording:** Records ambient sound through the microphone.
- **Screenshots:** Takes periodic screenshots of the system.
- **Encryption:** Encrypts the collected data to protect sensitive information.
- **Decryption:** Allows encrypted files to be decrypted for recovery of the logged data.

## Requirements
- Python 3.x
- `cryptography`
- `pynput`
- `sounddevice`
- `scipy`
- `Pillow`
- `pywin32` (for Windows users)
You can install the necessary dependencies using `pip`:
```bash
  pip install cryptography pynput sounddevice scipy Pillow pywin32 requests
```
## Setup
**1. Clone the repository:**
```bash
  git clone https://github.com/AIwolfie/LunarLogger.git
```
**2.Generate the encryption key:**
Run the `KeyGenius.py` script to generate an encryption key.
```bash
  python KeyGenius.py
```
- The key will be saved in the `secure_key.bin` file. This key will be used to encrypt and decrypt the data.

**3.Running the Keylogger:**
After generating the key, run the keylogger to start logging
```bash
  python LunarLogger.py
```
- The script will begin logging keystrokes, taking screenshots, recording audio, and more.
- Logs will be encrypted and saved securely in specified files.

**4.Decrypting the Files:**
If you want to view the collected data, use the `Unlocker.py` script to decrypt the files.
```bash
  python Unlocker.py
```
- The decrypted data will be saved in new files.

## Security & Ethics
- **Encryption:** All logged data is encrypted before it is saved or sent to ensure confidentiality.
- **Use Responsibly:** Always get explicit consent before using this tool on any system. Unauthorized use of keyloggers is a violation of privacy and against the law.

## Contributing
- If you would like to contribute, feel free to fork the repository, create a branch, and submit a pull request.

## Disclaimer
This tool is for educational purposes only. The creator of this tool is not responsible for any illegal or unethical activities. Always follow legal and ethical guidelines when using such tools.

## Author

- [@Aiwolfie](https://github.com/AIwolfie)

<a href="https://www.buymeacoffee.com/mayankmalac" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
