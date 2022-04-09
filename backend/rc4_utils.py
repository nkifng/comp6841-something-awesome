# pseudocode taken from Wikipedia

SIZE = 256

# key scheduling algorithm
def KSA(key): 
    S = list(range(SIZE))  # S[i] := i
    j = 0
    for i in range(SIZE):
        j = (j + S[i] + key[i % len(key)]) % SIZE
        S[i], S[j] = S[j], S[i] # swap S[i] and S[j]
    return S

# pseudo random generation algorithm 
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % SIZE
        j = (j + S[i]) % SIZE
        S[i], S[j] = S[j], S[i] # swap S[i] and S[j]
        K = S[(S[i] + S[j]) % SIZE]
        yield K

def rc4_algorithm(key, fileName, outputName):
    key = [ord(c) for c in key]
    keyStream = PRGA(KSA(key))
    with open(fileName, "rb") as fIn:
        image = fIn.read()
        image = bytearray(image)
        for i, v in enumerate(image):
            image[i] = v ^ next(keyStream)
    with open(outputName, "wb") as fOut:
        fOut.write(image)

def rc4_encrypt(fileName, key):
    newName = fileName[:fileName.find(".")] + "_enc.png"
    rc4_algorithm(key, fileName, newName)
    return newName[(fileName.find("/") + 1):len(newName)]

def rc4_decrypt(fileName, key):
    newName = fileName[:fileName.find("_")] + "_dec" + fileName[(fileName.find(".")):len(fileName)]
    rc4_algorithm(key, fileName, newName)
    return newName[(fileName.find("/") + 1):len(newName)]
