from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Create a Fernet object with the key
fernet = Fernet(key)

# Encrypt a string
encrypted = fernet.encrypt(b"my secret data")

# Decrypt the string
decrypted = fernet.decrypt(encrypted)

# Print the decrypted string
print(decrypted.decode())