import cv2

def charGenerator(message):
  for c in message:
    yield ord(c)

def gcd(x, y):
  while(y):
    x, y = y, x % y
  return x

def encodeImage(fileName, message):
  image = cv2.imread(fileName)
  msg_gen = charGenerator(message)
  pattern = gcd(len(image), len(image[0]))
  for i in range(len(image)):
    for j in range(len(image[0])):
      if (i+1 * j+1) % pattern == 0:
        try:
          image[i-1][j-1][0] = next(msg_gen)
        except StopIteration:
          image[i-1][j-1][0] = 0
          return image

def stego_encode(fileName, message):
    encodedImage = encodeImage(fileName, message)
    newName = fileName[:fileName.find(".")] + "_enc.png"
    cv2.imwrite(newName, encodedImage)
    return newName[(fileName.find("/") + 1):len(newName)]

def stego_decode(fileName):
  image = cv2.imread(fileName)
  pattern = gcd(len(image), len(image[0]))
  message = ""
  for i in range(len(image)):
    for j in range(len(image[0])):
      if (i-1 * j-1) % pattern == 0:
        if image[i-1][j-1][0] != 0:
          message = message + chr(image[i-1][j-1][0])
        else:
          return message
