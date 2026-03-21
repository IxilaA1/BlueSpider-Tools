# (c) 2026 IxilaA1 - Tous droits réservés / All rights reserved / Todos los derechos reservados.
# Ce code ne peut être ni vendu, ni modifié, ni partagé sans autorisation, ni publié à votre nom.
# This code may not be sold, modified, or shared without authorization, nor published under your name.
# Este código no puede ser vendido, modificado ni compartido sin autorización, ni publicado a su nombre.
# -------------------------------------------------------------------------------------------------------
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

def derive_key(password_string, salt):
    """
    Derives a secure 32-byte encryption key (for AES-256) from the
    password (key) and the salt using PBKDF2.
    """
    password_bytes = password_string.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password_bytes)

def encrypt_message(message, key_string):
    """Encrypts a message using AES-256 in GCM mode (with salt and IV)."""
    
    
    salt = os.urandom(16)
    
    
    key = derive_key(key_string, salt)
    
    
    iv = os.urandom(12)
    
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    tag = encryptor.tag


    encrypted_data = salt + iv + ciphertext + tag
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_message(encrypted_b64, key_string):
    """Decrypts a message using AES-256 GCM."""
    
    
    try:
        encrypted_data = base64.b64decode(encrypted_b64)
    except:
        return "ERROR: Encrypted message is not a valid Base64 string."
    
    
    if len(encrypted_data) < 44: 
        return "ERROR: Encrypted message is too short or malformed."

    
    salt = encrypted_data[:16]
    iv = encrypted_data[16:28]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[28:-16]
    
    
    key = derive_key(key_string, salt)
    
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        decrypted_text_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text_bytes.decode('utf-8')
    except Exception as e:

        return f"ERROR: Decryption failed (Incorrect Key or Tampered data). Details: {e}"


def main():
    """Main function for the menu."""
    
    while True:
        print("\n--- AES Encryption/Decryption Tool (User Key) ---")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Quit")
        
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            print("\n--- ENCRYPTION MODE ---")
           
            key_input = input("Enter the SECRET KEY (e.g., 12345...): ")
            message = input("Enter the message to encrypt: ")
            
            encrypted_data = encrypt_message(message, key_input)
            
            print(f"\nOriginal Message: {message}")
            print(f"Key Used: {key_input[:5]}...{key_input[-5:]}")
            print(f"Encrypted Result (Base64): {encrypted_data}")
            
        elif choice == '2':
            print("\n--- DECRYPTION MODE ---")
            
            key_input = input("Enter the ORIGINAL SECRET KEY used for encryption: ")
            encrypted_message = input("Enter the encrypted message (Base64 string): ")
            
            decrypted_text = decrypt_message(encrypted_message, key_input)
            
            print(f"\nEncrypted Message: {encrypted_message}")
            print(f"Key Used: {key_input[:5]}...{key_input[-5:]}")
            print(f"Decrypted Result: {decrypted_text}")
            
        elif choice == '3':
            print("Exiting the encryption tool. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()