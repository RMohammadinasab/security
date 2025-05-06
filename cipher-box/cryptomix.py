import base64
from Crypto.Cipher import AES, DES, Salsa20, ChaCha20
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

# AES modes supported
AES_MODES = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "CFB": AES.MODE_CFB,
    "OFB": AES.MODE_OFB,
}

# Caesar Cipher
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) - offset + shift) % 26 + offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Morse Code
MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
                   'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
                   'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
                   'Z': '--..', ' ': '/', '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
                   '9': '----.', '0': '-----'}

def morse_encrypt(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def morse_decrypt(morse):
    reverse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return ''.join(reverse_dict.get(code, '') for code in morse.split())

# Hashing function
def hash_text(text, algorithm='sha256'):
    h = hashlib.new(algorithm)
    h.update(text.encode())
    return h.hexdigest()

# Transposition Cipher
def transpose_encrypt(text):
    return text[::-1]

def transpose_decrypt(text):
    return transpose_encrypt(text)

# Vernam Cipher
def vernam_encrypt(text, key):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(text, key))

def vernam_decrypt(text, key):
    return vernam_encrypt(text, key)

# Multiplicative Inverse Cipher
def multiplicative_inverse_encrypt(text, key):
    return ''.join(chr(((ord(char) - 32) * key % 95) + 32) for char in text)

def multiplicative_inverse_decrypt(text, key):
    for i in range(1, 95):
        if (key * i) % 95 == 1:
            inverse = i
            break
    else:
        raise ValueError("No multiplicative inverse exists.")
    return multiplicative_inverse_encrypt(text, inverse)

# AES Encryption
def aes_encrypt(text, key, mode='ECB'):
    key = key.encode('utf-8')[:16].ljust(16, b'0')
    mode = mode.upper()
    if mode == 'ECB':
        cipher = AES.new(key, AES_MODES[mode])
        ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(ciphertext).decode()
    else:
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES_MODES[mode], iv=iv)
        ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode()

# AES Decryption
def aes_decrypt(enc_text, key, mode='ECB'):
    key = key.encode('utf-8')[:16].ljust(16, b'0')
    mode = mode.upper()
    enc_bytes = base64.b64decode(enc_text)
    if mode == 'ECB':
        cipher = AES.new(key, AES_MODES[mode])
        decrypted = unpad(cipher.decrypt(enc_bytes), AES.block_size)
    else:
        iv = enc_bytes[:16]
        ciphertext = enc_bytes[16:]
        cipher = AES.new(key, AES_MODES[mode], iv=iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted.decode()

# DES
def des_encrypt(text, key):
    cipher = DES.new(key.encode('utf-8')[:8].ljust(8, b'0'), DES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(text.encode(), 8))
    return base64.b64encode(ct_bytes).decode()

def des_decrypt(enc_text, key):
    cipher = DES.new(key.encode('utf-8')[:8].ljust(8, b'0'), DES.MODE_ECB)
    return unpad(cipher.decrypt(base64.b64decode(enc_text)), 8).decode()

# Salsa20
def salsa_encrypt(text):
    key = get_random_bytes(32)
    cipher = Salsa20.new(key=key)
    ct = cipher.encrypt(text.encode())
    return base64.b64encode(cipher.nonce + ct).decode(), key

def salsa_decrypt(enc_text, key):
    enc = base64.b64decode(enc_text)
    nonce = enc[:8]
    ct = enc[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.decrypt(ct).decode()

# ChaCha20
def chacha_encrypt(text):
    key = get_random_bytes(32)
    cipher = ChaCha20.new(key=key)
    ct = cipher.encrypt(text.encode())
    return base64.b64encode(cipher.nonce + ct).decode(), key

def chacha_decrypt(enc_text, key):
    enc = base64.b64decode(enc_text)
    nonce = enc[:8]
    ct = enc[8:]
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ct).decode()

# Vigenère Cipher
def vigenere_encrypt(text, key):
    encrypted = ''
    key = key.upper()
    for i, char in enumerate(text):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(key[i % len(key)]) - 65
            encrypted += chr((ord(char) - offset + k) % 26 + offset)
        else:
            encrypted += char
    return encrypted

def vigenere_decrypt(text, key):
    decrypted = ''
    key = key.upper()
    for i, char in enumerate(text):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(key[i % len(key)]) - 65
            decrypted += chr((ord(char) - offset - k) % 26 + offset)
        else:
            decrypted += char
    return decrypted

# Main menu
def main():
    print("Welcome to the Encryption/Decryption Program")
    mode = input("Do you want to (E)ncrypt or (D)ecrypt? ").lower()
    text = input("Enter the text: ")

    print("""
Choose a method:
1. Caesar Cipher
2. Morse Code
3. Hashing (Encryption Only)
4. Transposition Cipher
5. Vernam Cipher
6. Multiplicative Inverse Cipher
7. DES
8. AES (Multiple Modes)
9. Salsa20
10. ChaCha20
11. Vigenère Cipher
    """)

    choice = input("Enter method number: ")

    if choice == '1':
        shift = int(input("Enter shift: "))
        result = caesar_encrypt(text, shift) if mode == 'e' else caesar_decrypt(text, shift)
    elif choice == '2':
        result = morse_encrypt(text) if mode == 'e' else morse_decrypt(text)
    elif choice == '3':
        algo = input("Enter hashing algorithm (e.g., sha256, md5): ")
        result = hash_text(text, algo)
    elif choice == '4':
        result = transpose_encrypt(text) if mode == 'e' else transpose_decrypt(text)
    elif choice == '5':
        key = input("Enter key of same length as text: ")
        result = vernam_encrypt(text, key) if mode == 'e' else vernam_decrypt(text, key)
    elif choice == '6':
        key = int(input("Enter key (must be coprime with 95): "))
        result = multiplicative_inverse_encrypt(text, key) if mode == 'e' else multiplicative_inverse_decrypt(text, key)
    elif choice == '7':
        key = input("Enter 8-byte key: ")
        result = des_encrypt(text, key) if mode == 'e' else des_decrypt(text, key)
    elif choice == '8':
        key = input("Enter 16-byte key: ")
        print("Available AES modes: ECB, CBC, CFB, OFB")
        aes_mode = input("Choose AES mode: ").upper()
        if aes_mode not in AES_MODES:
            print("Invalid AES mode.")
            return
        result = aes_encrypt(text, key, aes_mode) if mode == 'e' else aes_decrypt(text, key, aes_mode)
    elif choice == '9':
        if mode == 'e':
            result, key = salsa_encrypt(text)
            print(f"Encryption key (save it!): {base64.b64encode(key).decode()}")
        else:
            key = base64.b64decode(input("Enter base64-encoded key: "))
            result = salsa_decrypt(text, key)
    elif choice == '10':
        if mode == 'e':
            result, key = chacha_encrypt(text)
            print(f"Encryption key (save it!): {base64.b64encode(key).decode()}")
        else:
            key = base64.b64decode(input("Enter base64-encoded key: "))
            result = chacha_decrypt(text, key)
    elif choice == '11':
        key = input("Enter key: ")
        result = vigenere_encrypt(text, key) if mode == 'e' else vigenere_decrypt(text, key)
    else:
        print("Invalid method.")
        return

    print("Result:", result)

if __name__ == "__main__":
    main()
