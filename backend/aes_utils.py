from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def aes_encrypt(file_name, key):
    key = pad(key.encode("utf-8"), AES.block_size)
    with open(file_name, "rb") as fIn:
        data = fIn.read()
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        iv = b64encode(cipher.iv).decode('UTF-8')
        ciphertext = b64encode(ciphertext).decode('UTF-8')
        output = iv + ciphertext
    new_name = file_name[:file_name.find(".")] + "_enc" + file_name[(file_name.find(".")):len(file_name)]
    with open(new_name, "w") as fOut:
        fOut.write(output)
    return new_name[(file_name.find("/") + 1):len(new_name)]

def aes_decrypt(file_name, key):
    key = pad(key.encode("utf-8"), AES.block_size)
    try:
        with open(file_name, "r") as f:
            data = f.read()
            iv = b64decode(data[:24])
            ciphertext = b64decode(data[24:len(data)])
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted = cipher.decrypt(ciphertext)
            decrypted = unpad(decrypted, AES.block_size)
            new_name = file_name[:file_name.find("_")] + "_dec" + file_name[(file_name.find(".")):len(file_name)]
            with open(new_name, "wb") as outputFile:
                outputFile.write(decrypted)
        return new_name[(file_name.find("/") + 1):len(new_name)]
    except(ValueError, KeyError):
        return file_name