from PIL import Image
from PIL import ImageFilter
from PIL import *
import imagehash
import itertools
from Tkinter import Tk
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
import random
import os

BROJ_TRANSFORMACIJA = 9
VARIATION_COUNT = 5


def renameAllFilesInFolder(folderPath, fileName):
    """"
    :type folderPath:str
    :type fileName:str
    """
    i = 1
    for oldFileName in os.listdir(folderPath):
        print(oldFileName + "," + fileName + '[' + i.__str__() + ']')
        os.renames(folderPath + "/" + oldFileName, folderPath + "/" + fileName + '[' + i.__str__() + ']')
        i = i + 1
    return


def TransformAndSave(folderPath, image, imageName, generatedImagesCount):
    directoryPath = folderPath + "/" + "Transformations" + "/"
    if not os.path.exists(directoryPath):
        os.mkdir(directoryPath)

    for i in range(generatedImagesCount):
        transformedImage, suffix = RandTransform(image, random.randint(1, 4))
        completePath = directoryPath + imageName + suffix + ".png"

        transformedImage.save(completePath)


def RandTransform(image, transformationCount):
    suffix = ""

    transformationCount = min(transformationCount, BROJ_TRANSFORMACIJA)

    l = list()

    for i in range(0, BROJ_TRANSFORMACIJA):
        l.append(i)

    random.shuffle(l)

    result = image.copy()

    for i in range(0, transformationCount):
        transformationIndex = l[i]

        if transformationIndex == 0:
            result = RandomRotate(result)
            suffix += "_rotated"
        elif transformationIndex == 1:
            result = RandomCrop(result)
            suffix += "_cropped"
        elif transformationIndex == 2:
            result = RandomResize(result)
            suffix += "_resized"
        elif transformationIndex == 3:
            result = RandomBlur(result)
            suffix += "_blurred"
        elif transformationIndex == 4:
            result = RandomGaussianBlur(result)
            suffix += "_gaussianblurred"
        elif transformationIndex == 5:
            result = RandomSmooth(result)
            suffix += "_smoothen"
        elif transformationIndex == 6:
            result = RandomScale(result)
            suffix += "_scaled"
        elif transformationIndex == 7:
            result = RandomFlipLR(result)
            suffix += "_flipepdLR"
        elif transformationIndex == 8:
            result = RandomFlipTB(result)
            suffix += "_flipepdTB"
    return result, suffix


def RandomRotate(image):
    degrees = random.randint(0, 360)
    return image.rotate(degrees)


def RandomCrop(image):
    width, height = image.size
    x0 = random.randint(0, (int)(width * .75))
    y0 = random.randint(0, (int)(height * .75))
    x1 = random.randint((int)(x0 * 1.1), width)
    y1 = random.randint((int)(y0 * 1.1), height)
    return image.crop((x0, y0, x1, y1))


def RandomResize(image):
    width, height = image.size
    width = random.randint((int)(.1 * width), (int)(.9 * width))
    height = random.randint((int)(.1 * height), (int)(.9 * height))
    return image.resize((width, height))


def RandomBlur(image):
    """""
    :type image:Image
    """""
    return image.filter(ImageFilter.BLUR)


def RandomGaussianBlur(image):
    """""
    :type image:Image
    """""
    return image.filter(ImageFilter.GaussianBlur(random.randint(0, 15)))


def RandomSmooth(image):
    """""
    :type image:Image
    """""
    return image.filter(ImageFilter.SMOOTH)


def RandomScale(image):
    """""
    :type image:Image
    """""
    width, height = image.size
    max = min(width, height)
    maxsize = (max, max)
    image.thumbnail(maxsize, Image.ANTIALIAS)
    return image


def RandomFlipLR(image):
    """""""""
    :type image:Image
    """""""""
    return image.transpose(Image.FLIP_LEFT_RIGHT)


def RandomFlipTB(image):
    """""""""
    :type image:Image
    """""""""
    return image.transpose(Image.FLIP_TOP_BOTTOM)


"""""
TODO: MAYBE ADD NOISE TO IMAGE
"""""
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
folderPath = askdirectory(initialdir="/home/")
for file in os.listdir(folderPath):
    transformationFolder = os.path.abspath(os.path.join(folderPath, os.pardir))
    fullFilePath = folderPath + '/' + file
    if (os.path.isdir(fullFilePath)):
        continue

    TransformAndSave(transformationFolder, Image.open(fullFilePath), file, VARIATION_COUNT)
