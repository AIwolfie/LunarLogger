from cryptography.fernet import Fernet

def generate_encryption_key():
    key = Fernet.generate_key()  # Create a key for encryption
    with open("secure_key.bin", 'wb') as key_file:
        key_file.write(key)  
    print("Encryption key has been generated and saved to secure_key.bin")

if __name__ == "__main__":
    generate_encryption_key() 
