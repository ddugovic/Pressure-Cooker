# IMPORT
from settings import ChoreInstructions
from settings import CookRegion
from settings import FoodRecipe
from settings import HSRegion
from settings import ServeRegion
from settings import ServingKeyBinds
from settings import SpecialKeyBinds
from settings import TextRegions
from settings import WindowGame
import cv2
import mss
import numpy as np
import pytesseract
import pyautogui
import random
import re
import time

# FUNCTIONS


# Define function to extract a region of the game window
def WindowExtractor(BigWindow, WindowBounds, BoundNumX, BoundNumY):
    return BigWindow[WindowBounds['top'][BoundNumY]: WindowBounds['top'][BoundNumY]+WindowBounds['height'],
                     WindowBounds['left'][BoundNumX]: WindowBounds['left'][BoundNumX]+WindowBounds['width'], :]


# Define function to threshold and determine number of recipes for the holding stations
def TextScanHoldingStationOpts(ImgGame, WindowBounds):
    # Take image and binarise to extract detail
    ImgFoodInputBig = ImgGame
    ImgFoodInputBig[(ImgFoodInputBig[:, :, 0] == ImgFoodInputBig[:, :, 1]) &
                    (ImgFoodInputBig[:, :, 0] == ImgFoodInputBig[:, :, 2])] = 255
    WindowBig = [ImgFoodInputBig != [255, 255, 255]][0].astype('uint8') * 255

    # Window out chores?

    # Find all avaliable keypresses
    RecipeOpts = []
    for loopImgFindx in range(0, len(TextRegions['left'])):
        for loopImgFindy in range(0, len(TextRegions['top'])):
            ImgInput = WindowExtractor(WindowBig, WindowBounds, loopImgFindx, loopImgFindy)

            FoundThing = pytesseract.image_to_string(ImgInput[:, :, 0], config='-psm 10')

            # Add code here to deal with chores

            # Turn into parsed raw text
            if FoundThing != '':
                RecipeOpts.append(FoundThing)
    return(RecipeOpts)


# Define function to follow through recipe finding & creation
def FoodMaker(ImgInstructionInputBig, WindowRegion, ColorBlobSize):
    # Threshold and scan for instructions
    RawInstruction = TextScanRecipe(ImgInstructionInputBig, WindowRegion, ColorBlobSize)
    print('            Raw Text: ' + str(RawInstruction[0]))

    # Build out list to perform
    AllInstructions = InstructionMaker(RawInstruction)
    print('            Instructions: ' + " ".join(str(elm) for elm in AllInstructions))

    # Perform instructions
    InstructionFollower(AllInstructions)
    time.sleep(0.1)


# Define function to threshold and determine ingredients avaliable for a recipe
def TextScanRecipe(ImgInstructionInputBig, FoodRecipe, ColorBlobSize):
    ImgInstructionRGB = WindowExtractor(ImgInstructionInputBig, FoodRecipe, 0, 0)
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


# Define function to build a set of instructions to follow
def InstructionMaker(RawInstruction):
    RecipeInstructions = []

    # If chore:
    if RawInstruction[0] in ChoreInstructions:
        RecipeInstructions = ChoreInstructions[RawInstruction[0]]

    # If not chore:
    else:
        for IngredientItem in RawInstruction[0].split("  "):

            # Get ingredient name
            Ingredient = IngredientItem.split(" (")[0]

            # Get number of repeat keypresses
            RepeatSearch = re.search(r'[0-9]', IngredientItem)
            if RepeatSearch:
                RepeatNum = int(RepeatSearch.group(0))
            else:
                RepeatNum = 1

            # Get key to press: if not in special list, just take first letter
            if Ingredient in SpecialKeyBinds:
                KeyCombo = SpecialKeyBinds[Ingredient]
            else:
                KeyCombo = Ingredient[0].lower()

            # Build the instruction!
            RecipeInstructions.append([Ingredient, RepeatNum, KeyCombo])

        # Add in instructions to go to new page if neccessary
        if RawInstruction[1][1] == 0 & RawInstruction[1][0] != 0 & RawInstruction[1][2] != 0:
            NumFilled = 2
        else:
            NumFilled = sum(x != 0 for x in RawInstruction[1]) - 1
        RawInstructionFilt = RawInstruction[1][0: NumFilled]
        for SpaceInsert in RawInstructionFilt[:: -1]:
            RecipeInstructions.insert(SpaceInsert, ['NextPage', 1, 'space'])

    # Return
    return(RecipeInstructions)


# Define function to follow instructions
def InstructionFollower(AllInstructions):
    # Follow instructions in list
    for Instruction in AllInstructions:
        for PressKey in range(0, Instruction[1]):
            pyautogui.keyDown(Instruction[2])
            pyautogui.keyUp(Instruction[2])

    # Finish recipe
    pyautogui.press('enter')


# Define function to prepare a holding station from a list of recipes
def PrepareHoldingStation(sct, ColorBlobSize, station, PauseTime, AllRecipeOpts, DoneOpts1, DoneOpts2, DoneOpts11, DoneOpts22):
    # Open the holding station (can't use.hotkey because of releasing keys backwards)
    pyautogui.keyDown('tab')
    time.sleep(PauseTime)
    pyautogui.keyDown(str(station+1))
    time.sleep(PauseTime)
    pyautogui.keyUp('tab')
    time.sleep(PauseTime)
    pyautogui.keyUp(str(station+1))

    # Create list of already completed options, but remove from list
    # if we are revisiting the Holding Station that option was made in
    for RemoverLoop1 in DoneOpts11:
        if RemoverLoop1[1] == station+1:
            DoneOpts1.remove(RemoverLoop1[0])
            DoneOpts11.remove(RemoverLoop1)
    for RemoverLoop2 in DoneOpts22:
        if RemoverLoop2[1] == station+1:
            DoneOpts2.remove(RemoverLoop2[0])
            DoneOpts22.remove(RemoverLoop2)
    FiltOpts1 = set(AllRecipeOpts[0]) - set(DoneOpts1)
    FiltOpts2 = set(AllRecipeOpts[1]) - set(DoneOpts2)

    # Pick a recipe
    HoldingStationWindowNum = 1
    if (HoldingStationWindowNum == 1) & (bool(FiltOpts1) == 1) & (len(AllRecipeOpts[0]) > 0):
        # Make a Holding Station required recipe
        print('    Making a Holding Station required recipe')
        randopt = random.sample(FiltOpts1, 1)[0].lower()
        DoneOpts1.append(randopt.upper())
        DoneOpts11.append([randopt.upper(), station+1])

    elif (bool(FiltOpts1) == 0):
        print('    All Holding Station required recipes made')
        HoldingStationWindowNum += 1
        pyautogui.hotkey('space')
        RecipeOpts = AllRecipeOpts[1]
        if (HoldingStationWindowNum == 2) & (bool(FiltOpts2) == 1) & (len(AllRecipeOpts[1]) > 0):
            # Make a Holding Station optional recipe
            print('    Making a Holding Station optional recipe')
            randopt = random.sample(FiltOpts2, 1)[0].lower()
            DoneOpts2.append(randopt.upper())
            DoneOpts22.append([randopt.upper(), station+1])

        elif (len(AllRecipeOpts[2]) > 0):
            # Make a side
            print('    All Holding Station optional recipes made \n    Making a side')
            RecipeOpts = AllRecipeOpts[2]
            HoldingStationWindowNum += 1
            pyautogui.hotkey('space')
            randopt = random.sample(RecipeOpts, 1)[0].lower()

        else:
            print('    Nothing to make in a Holding Station!')
            return

    # Start the recipe!!!
    print('        Making Recipe ' + randopt.upper())
    pyautogui.keyDown(randopt)
    pyautogui.keyUp(randopt)
    time.sleep(0.1)

    # Get image
    ImgInstructionInputBig = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
    FoodMaker(ImgInstructionInputBig, FoodRecipe, ColorBlobSize)

    # Clear holding station if food has spoiled


# Define function to prepare a holding station from a list of recipes
def Serve(sct, ImgServeRegion, serviceStation, PauseTime):
    # Determine if food can be served, or is currently cooking
    if np.sum(cv2.inRange(ImgServeRegion, np.array([255, 255, 255]), np.array([255, 255, 255]))) > 45000:

        # If food is currently cooking, do nothing
        print('    Blocked/Waiting for Cooking.')
    else:
        # Attempt to insta-serve
        pyautogui.keyDown(ServingKeyBinds[str(serviceStation+1)])
        time.sleep(PauseTime)
        pyautogui.keyUp(ServingKeyBinds[str(serviceStation+1)])

        colorRGB = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
        ImgInstaTester = WindowExtractor(colorRGB, FoodRecipe, 0, 0)
        if np.sum(cv2.inRange(ImgInstaTester, np.array([73, 73, 73]), np.array([73, 73, 73]))) < 1000:
            print('        Food insta-served')
        else:
            # If extra steps required
            print('        Extra steps required')
            ImgInstructionInputBig = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
            FoodMaker(ImgInstructionInputBig, FoodRecipe)


def main():
    # Set stuff up
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    sct = mss.mss()
    HoldingStation_Capturing = 1
    # ImgHSRegion = np.zeros([HSRegion['height'], HSRegion['width'], 3, len(HSRegion['left'])]).astype('uint8')
    ImgServe = np.zeros([ServeRegion['height'], ServeRegion['width'], 3, len(ServeRegion['top'])]).astype('uint8')
    DoneOpts1 = []
    DoneOpts2 = []
    DoneOpts11 = []
    DoneOpts22 = []
    AllRecipeOpts = []
    pyautogui.PAUSE = 0.08
    PauseTime = 0.12
    ColorBlobSize = 155040  # Number of pixels a purple/red/yellow blow takes up

    # DETERMINE Holding Station OPTIONS

    # Find and store holding station options
    while HoldingStation_Capturing == 1:
        # Take constant images of screen until a Holding Station appears
        ImgGameWindow = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
        if int(np.round(np.mean(WindowExtractor(ImgGameWindow, HSRegion, 1, 0)))) in range(36, 40):
            # Open the holding station
            print('Capturing holding station data!')
            pyautogui.keyDown('tab')
            time.sleep(PauseTime)
            pyautogui.keyDown('1')
            time.sleep(PauseTime)
            pyautogui.keyUp('tab')
            time.sleep(PauseTime)
            pyautogui.keyUp('1')

            # OCR for each page of the holding station, and store results
            for loopRecipeBuilder in range(0, 3):
                ImgCapt = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
                AllRecipeOpts.append(TextScanHoldingStationOpts(ImgCapt, TextRegions))
                pyautogui.keyDown('space')
                pyautogui.keyUp('space')
                HoldingStation_Capturing = 0

            # Leave holding station
            pyautogui.keyDown('enter')
            pyautogui.keyUp('enter')
            break

    # Start with a side to increase waiting time
    pyautogui.keyDown('tab')
    time.sleep(PauseTime)
    pyautogui.keyDown('6')
    time.sleep(PauseTime)
    pyautogui.keyUp('tab')
    time.sleep(PauseTime)
    pyautogui.keyUp('6')
    pyautogui.hotkey('space')
    pyautogui.hotkey('space')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    time.sleep(0.1)

    # Get image
    ImgInstructionInputBig = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)
    FoodMaker(ImgInstructionInputBig, FoodRecipe)

    # A NEW DAWN OF FEASTING IS AT HAND
    start_time = time.time()
    while 'Screen capturing':
        # Get raw pixels from the screen, save it to a numpy array
        ImgGameWindow = cv2.cvtColor(np.array(sct.grab(WindowGame)), cv2.COLOR_RGBA2RGB)

        # For each holding station (but not at rush hour)
        elapsed_time = time.time() - start_time
        if elapsed_time < 90 or int(elapsed_time) in range(160, 250) or elapsed_time > 310:
            for holdingStation in range(0, len(HSRegion['left'])):

                # Check if a Holding Station is free
                ImgWindowHoldingStation = WindowExtractor(ImgGameWindow, HSRegion, holdingStation, 0)
                if int(np.round(np.mean(ImgWindowHoldingStation))) in range(36, 40):
                    print('\nHolding Station ' + str(holdingStation + 1) + ' Free!')
                    PrepareHoldingStation(sct, ColorBlobSize, holdingStation, PauseTime,
                                          AllRecipeOpts, DoneOpts1, DoneOpts2, DoneOpts11, DoneOpts22)

        for serviceStation in range(0, len(ServeRegion['top'])):
            # Check if a serving region requires service
            ImgServe = WindowExtractor(ImgGameWindow, ServeRegion, 0, serviceStation)
            if np.sum(ImgServe == [255, 255, 255]) > 0:
                print('\nServing Station ' + str(serviceStation + 1) + ' Occupied!')

                # Get section of screen
                ImgServeRegion = WindowExtractor(ImgGameWindow, CookRegion, 0, serviceStation)
                Serve(sct, ImgServeRegion, serviceStation, PauseTime)

    # Need to look for burning food and prioritise it!


if __name__ == "__main__":
    # execute only if run as a script
    main()
