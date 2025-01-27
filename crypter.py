from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import os
import getpass

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def derive_key_and_iv(keyphrase, salt, key_length, iv_length):
    # Derive the key and IV using PBKDF2
    dkey = PBKDF2(keyphrase, salt, dkLen=key_length + iv_length, count=1000000)
    return dkey[:key_length], dkey[key_length:key_length + iv_length]

def encrypt_file(input_file, output_file, keyphrase):
    try:
        salt = get_random_bytes(16)  # 128-bit salt
        key, iv = derive_key_and_iv(keyphrase, salt, 32, AES.block_size)

        cipher = AES.new(key, AES.MODE_CBC, iv)

        with open(input_file, 'rb') as f:
            plaintext = f.read()

        padded_data = pad(plaintext, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)

        with open(output_file, 'wb') as f:
            content = salt + encrypted_data
            f.write(content)

        print("File encrypted successfully.")
    except Exception as e:
        print(e)

def decrypt_file(input_file, output_file, keyphrase):
    try:
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()

        salt = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        key, iv = derive_key_and_iv(keyphrase, salt, 32, AES.block_size)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(output_file, 'wb') as f:
            f.write(decrypted_data)

        print("File decrypted successfully.")
        
    except Exception as e:
        print(e)

def shred_file(file_path, passes=3):
    """
    Securely delete a file by overwriting it with random data.

    :param file_path: The path to the file to be shredded.
    :param passes: The number of times the file is overwritten with random data.
    """
    if os.path.isfile(file_path):
        with open(file_path, 'ba+', buffering=0) as f:
            length = f.tell()
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(file_path)
        print(f"{file_path} has been securely deleted.")
    else:
        print(f"File {file_path} does not exist.")


if __name__ == "__main__":

    try:
        print(f"Enter command - [{BLUE}what,{GREEN}where from, {YELLOW}where to]{BLUE}")
        command = input()
        command = command.split(' ')
        print("Enter key")
        keyphrase = getpass.getpass()

        if command[0] == 'encrypt' or command[0] == 'e':
            if len(command) < 3:
                command.append(command[1].split('.')[0] + '.bin')
            encrypt_file(command[1], command[2], keyphrase)
        elif command[0] == 'decrypt' or command[0] == 'd':
            if len(command) < 3:
                command.append(command[1].split('.')[0] + '.txt')
            decrypt_file(command[1], command[2], keyphrase)
        elif command[0] == 'shred' or command[0] == 's':
            shred_file(command[1])
    except e as Exception:
        print("Unable to procede")
        print(e)
