from PIL import Image
from encrypt import AES
from decrypt import AESDecrypt
from RSA import RSA
import random
import string

def generate_random_key(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def encrypt_main():
    # Generate a random AES key
    aes_key = generate_random_key()
    
    # Initialize RSA
    rsa = RSA()
    
    # Encrypt the AES key using RSA
    encrypted_key = [rsa.encrypt(ord(char)) for char in aes_key]
    
    # Initialize AES with the generated key
    aes = AES(aes_key)
    
    # Open and encrypt the image
    image_path = 'Cs202-21.jpg'
    img = Image.open(image_path)
    img_bytes = img.tobytes()
    img_size = img.size
    img_mode = img.mode
    
    encrypted_bytes = aes.encrypt(img_bytes)
    encrypted_img = Image.frombytes(img_mode, img_size, encrypted_bytes)
    encrypted_img.save('encrypted_image.png')
    
    # Save the encrypted key
    with open('encrypted_key.txt', 'w') as f:
        f.write(','.join(map(str, encrypted_key)))
    
    print("Image encrypted and saved as 'encrypted_image.png'")
    print("Encrypted key saved in 'encrypted_key.txt'")

def decrypt_main():
    # Initialize RSA
    rsa = RSA()
    
    # Read the encrypted key
    with open('encrypted_key.txt', 'r') as f:
        encrypted_key = list(map(int, f.read().split(',')))
    
    # Decrypt the AES key
    decrypted_key = ''.join(chr(rsa.decrypt(char)) for char in encrypted_key)
    
    # Initialize AES decryption with the decrypted key
    aes_decrypt = AESDecrypt(decrypted_key)
    
    # Open and decrypt the image
    image_path = 'encrypted_image.png'
    img = Image.open(image_path)
    img_bytes = img.tobytes()
    img_size = img.size
    img_mode = img.mode
    
    decrypted_bytes = aes_decrypt.decrypt(img_bytes)
    restored_img = Image.frombytes(img_mode, img_size, decrypted_bytes)
    restored_img.save('decrypted_image.png')
    
    print("Image decrypted and saved as 'decrypted_image.png'")

if __name__ == "__main__":
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ").lower()
    if choice == 'e':
        encrypt_main()
    elif choice == 'd':
        decrypt_main()
    else:
        print("Invalid choice. Please enter 'e' or 'd'.")