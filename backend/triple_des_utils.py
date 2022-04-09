from Crypto.Cipher import DES3
from hashlib import md5

def triple_des_encrypt(fileName, key):
    keyHash = md5(key.encode("ascii")).digest()
    tdesKey = DES3.adjust_key_parity(keyHash)
    cipher = DES3.new(tdesKey, DES3.MODE_EAX, nonce=b'0')
    with open(fileName, 'rb') as inputFile:
        fileBytes = inputFile.read()
        encrypted = cipher.encrypt(fileBytes)
    inputFile.close()
    newName = fileName[:fileName.find(".")] + "_enc" + fileName[(fileName.find(".")):len(fileName)]
    with open(newName, "wb") as outputFile:
        outputFile.write(encrypted)
    outputFile.close()
    return newName[(fileName.find("/") + 1):len(newName)]


def triple_des_decrypt(fileName, key):
    keyHash = md5(key.encode("ascii")).digest()
    tdesKey = DES3.adjust_key_parity(keyHash)
    cipher = DES3.new(tdesKey, DES3.MODE_EAX, nonce=b'0')
    try:
        with open(fileName, 'rb') as inputFile:
            fileBytes = inputFile.read()
            decrypted = cipher.decrypt(fileBytes)
        inputFile.close()
        newName = fileName[:fileName.find("_")] + "_dec" + fileName[(fileName.find(".")):len(fileName)]
        with open(newName, "wb") as outputFile:
            outputFile.write(decrypted)
        outputFile.close()
        return newName[(fileName.find("/") + 1):len(newName)]
    except(ValueError, KeyError):
       return fileName