import numpy as np
import cv2

def logisticKey(x, r, size):
    key = []

    for i in range(size):   
        x = r * x * (1 - x)   # logistic equation
        key.append(int((x * pow(10, 16)) % 256))  

    return key


def chaos_map_encode(fileName):
    image = cv2.imread(fileName)
    height, width, _ = image.shape
    generatedKey = logisticKey(0.01, 3.95, height * width) 
    z = 0
    encryptedImage = np.zeros(shape=[height, width, 3], dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            # Using the XOR operation between image pixels and keys
            encryptedImage[i, j] = image[i, j].astype(int) ^ generatedKey[z]
            z += 1
    newName = fileName[:fileName.find(".")] + "_enc.png"
    cv2.imwrite(newName, encryptedImage)
    return newName[(fileName.find("/") + 1):len(newName)]


def chaos_map_decode(fileName):
    image = cv2.imread(fileName)
    height, width, _ = image.shape
    z = 0
    decryptedImage = np.zeros(shape=[height, width, 3], dtype=np.uint8)
    generatedKey = logisticKey(0.01, 3.95, height * width)
    for i in range(height):
        for j in range(width):
            # Using the XOR operation between encrypted image pixels and keys
            decryptedImage[i, j] = image[i, j].astype(int) ^ generatedKey[z]
            z += 1
    newName = fileName[:fileName.find("_")] + "_dec" + fileName[(fileName.find(".")):len(fileName)]
    cv2.imwrite(newName, decryptedImage)
    return newName[(fileName.find("/") + 1):len(newName)]