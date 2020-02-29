# IMPORT
import pyautogui
import random
import time


# Define function to follow instructions
def execute(AllInstructions):
    # Follow instructions in list
    for Instruction in AllInstructions:
        for PressKey in range(0, Instruction[1]):
            pyautogui.keyDown(Instruction[2])
            pyautogui.keyUp(Instruction[2])

    # Finish recipe
    pyautogui.press('enter')


# Define function to reset the game state
def reset(PauseTime):
    pyautogui.keyDown('tab')
    time.sleep(PauseTime)
    pyautogui.keyDown('1')
    time.sleep(PauseTime)
    pyautogui.keyUp('tab')
    time.sleep(PauseTime)
    pyautogui.keyUp('1')


# Define function to prepare a side
def side(PauseTime):
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


# Define function to prepare a holding station from a list of recipes
def prepare(sct, ColorBlobSize, station, PauseTime, AllRecipeOpts, DoneOpts1, DoneOpts2, DoneOpts11, DoneOpts22):
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


# Define function to serve food from a service station
def serve(ServingKeyBinds, serviceStation, PauseTime):
    pyautogui.keyDown(ServingKeyBinds[str(serviceStation+1)])
    time.sleep(PauseTime)
    pyautogui.keyUp(ServingKeyBinds[str(serviceStation+1)])
