# IMPORT
import cv2
import numpy as np
import pytesseract


# Define function to threshold and determine number of recipes for the holding stations
def read(ImgInput):
    return pytesseract.image_to_string(ImgInput[:, :, 0], config='-psm 10')


# Define function to threshold and determine ingredients avaliable for a recipe
def read_recipe(ImgInstructionRGB, FoodRecipe, ColorBlobSize):
    ImgInstruction = cv2.cvtColor(ImgInstructionRGB, cv2.COLOR_RGB2GRAY)
    # Get number of purple, red, yellow instructions
    NumPurple = np.sum(cv2.inRange(ImgInstructionRGB, np.array([201, 65, 122]), np.array([201, 65, 122])))
    NumRed = np.sum(cv2.inRange(ImgInstructionRGB, np.array([65, 65, 201]), np.array([65, 65, 201])))
    NumYellow = np.sum(cv2.inRange(ImgInstructionRGB, np.array([41, 138, 189]), np.array([41, 138, 189])))
    PageNums = [int(np.round(NumPurple / ColorBlobSize)),
                int(np.round(NumRed / ColorBlobSize)),
                int(np.round(NumYellow / ColorBlobSize))]

    # Get raw instruction
    ImgInstruction[ImgInstruction == 213] = 255
    ImgInstruction[ImgInstruction == 192] = 255
    ImgInstruction[ImgInstruction != 255] = 0
    RawInstruction = pytesseract.image_to_string(ImgInstruction, config='-psm 11').replace('\n', ' ').replace('ENTER', '')
    return(RawInstruction, PageNums)


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
