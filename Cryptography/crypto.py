import random

def text_to_binary(text):
    """ Encodes each letter and/or symbol into binary. """

    binary = " ".join(format(ord(c), "b") for c in text)

    return binary


def binary_to_text(binary):
    """ Decodes each bit into the letters and/or symbols. """

    plaintext = "".join(chr(int(c, 2)) for c in binary.split(" "))

    return plaintext


def generate_key(binary):
    """ Generates a random one-time pad key based on binary length. """

    key = ''
    for num in binary:
        if (num == '0') or (num == '1'):
            new_num = random.randint(0,1)
            key += str(new_num)
        else:
            key += ' '

    return key


def XOR(str1, str2):
    """ Combines two strings into using the 'exclusive or' one-time pad encryption """    

    index = 0
    combined_str = ''
    while index <= len(str1) - 1:
        if (str1[index] == ' ') and (str2[index] == ' '):
            combined_str += ' '
            index += 1
        elif (str1[index] == '0' and str2[index] == '0') or (str1[index] == '1' and str2[index] == '1'):
            combined_str += '0'
            index += 1
        elif (str1[index] == '1' and str2[index] == '0') or (str1[index] == '0' and str2[index] == '1'):
            combined_str += '1'
            index += 1
    
    return combined_str


def save_to_drive(name, key):
    """ Saves one-time pad key to designated drive. """

    with open(f"F:/Keys/{name}.txt", "w") as f:
        f.write(key)


def retrieve_key_and_password(name, ciphertext):
    """ Retrieves key and decrypts ciphertext into plaintext password. """

    with open(f"F:/Keys/{name}.txt", "r") as f:
        key = f.readline()
    password_bytes = XOR(key, ciphertext)
    password = binary_to_text(password_bytes)

    return password
