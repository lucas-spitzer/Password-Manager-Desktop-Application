import pyotp
import qrcode


def generate_key():
    ''' Generates a key to be written into a .txt file and used during "authentication_setup" and "verify_2FA_code" functions. '''

    KEY = pyotp.random_base32()  # Randomly generates a constant global variable as a key to be utilized in later in the script. 
    with open('twoFA/key.txt', 'w') as file:  # Opens and writes key into 'key.txt' within the 'twoFA' folder.
        file.write(KEY)


def retrieve_key():
    ''' Reads and returns key from "key.txt" file. '''

    with open('twoFA/key.txt', 'r') as file:  # Opens and Reads 'key.txt' within the 'twoFA' folder.
        KEY = file.read()
    return KEY  # Returns 'KEY' as a string variable.


def authentication_setup():
    ''' Uses randomly generated key above to create QR Code for Google Authenicator App. 
    Once created, scan with your phone to successfully setup 2-Factor Authentication. '''

    KEY = retrieve_key()  # Retrieves key from 'key.txt' file as a string.
    uri = pyotp.totp.TOTP(KEY).provisioning_uri(name = "Lucas Spitzer", issuer_name = "Password Manager")  # Provides params to create a URI for 2FA App.
    qrcode.make(uri).save("twoFA/pyotp-qrcode.png")  # Creates 'pyotp-qrcode.png' file to be scanned using Google Authenticator App.


def verify_2FA_code(code):
    ''' Verifies whether a given code resembles its totp counterpart. This function will be imported and utilized in "main.py". '''

    KEY = retrieve_key()  # Retrieves key from .txt file as a string.
    totp = pyotp.TOTP(KEY)  # Reformats key to prepare for verify method.
    return totp.verify(code)  # Returns True or False based on if the code provided is valid.


def main():
    ''' This file is setup so the user can run this function once, scan the QR code, and utilize the Google Authenticator on another device. '''

    generate_key()  # Generates 2FA key as 'key.txt' in the 'twoFA' folder.
    authentication_setup()  # Creates QR code as 'pyotp-qrcode.png' in the 'twoFA' folder.


if __name__=="__main__":
    main()
