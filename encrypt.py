from AesEverywhere import aes256

SECRET_KEY = "d3ad5b824759ab7dc80c5a9f9527989c"


def decrypt(text: str) -> str:
    """ Decryption encrypted text """
    decryption = aes256.decrypt(text, SECRET_KEY)
    result = str(decryption)[2:-1]
    return result


def encrypt(text: str) -> str:
    """ Encryption encrypted text """
    encrypted = aes256.encrypt(text, SECRET_KEY)
    return encrypted


message = "hello"

enc = encrypt(text=message)
print("ENC........", enc)

dec = decrypt(text=enc)
print("DEC........", dec)