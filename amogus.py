import pyautogui
from time import sleep
from PIL import Image
import cv2 as cv
import numpy as np
import easyocr
import ollama
import subprocess
import random
import pyscreeze
import re

if __name__ == "__main__":
    """
    initialise ocr tesseract reader
    """
    reader = easyocr.Reader(['en'])

    """
    initialise variables
    information: an list of strings that can be used to store 'information' e.g position and what it sees
    bot_messages: list of strings used to store messages FROM the bot
    chat_messages: list of strings used to store 'chat messages', basically what it sees on screen when it takes a screenshot
    imposter: a dynamic value which is set whenever the imposter or crewmate screen is seen
    messages: this is what is actually fed to the bot, strings are taken from OTHER lists and put here when needed
    model: llm model used (stored as string)

    game_state: unused
    colors: all the possible colors a player can be
    possible_votes: all the possible locations a vote can be in
    PAUSE value: this is how long it waits after every update
    moving: a bool used for debugging, whether it should have any movement or not
    NEUTRAL: a constant for a safe place to put the mouse cursor
    """

    screen_height, screen_width = 2560, 1600

    pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
    pyautogui.FAILSAFE = False

    information = []
    bot_messages = []
    chat_messages = []
    imposter = False
    messages = [{"role": "system", "content": open("prompt_message.txt", "r").read()}]
    up, left, down, right = "w", "a", "s", "d"

    model = "hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF:Q8_0"
    model = "hf.co/mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated-GGUF:Q8_0"
    model = "hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF:Q8_0"

    game_state = None
    colors = ["Red", "Blue", "Green", "Pink", "Orange", "Yellow", "Black", "White", "Purple", "Brown", "Cyan", "Lime", "Maroon", "Rose", "Banana", "Gray", "Tan", "Coral", "skip"]
    possible_votes = [(655, 410), (1377, 410), (2116, 410), 
                      (655, 610), (1377, 610), (2116, 610), 
                      (655, 800), (1377, 800), (2116, 800), 
                      (655, 970), (1377, 970), (2116, 970), 
                      (655, 1165), (1377, 1165), (2116, 1165),
                      (453, 1345), (659, 1345)]
    
    pyautogui.PAUSE = 0.01

    moving = True
    NEUTRAL = (1000, 1000)
    
    """
    after initialising variables, start the ollama server so we can actually communicate with it, using the subprocess library
    """
    subprocess.Popen(["ollama", "serve"])
    subprocess.Popen(["ollama", "pull", model])
    print("started")
    
    
    while True:
        """
        here is the checking for the menu items, such as exiting, playing, and finding games
        """
        if pyautogui.locateCenterOnScreen('menu/exit_game.png', confidence=.95) != None: #no host
            sleep(10)
            if pyautogui.locateCenterOnScreen('menu/exit_game.png', confidence=.95) != None:
                pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/exit_game.png', confidence=.95))
                sleep(0.05)
                pyautogui.click()

        if pyautogui.locateCenterOnScreen('menu/play.png', confidence=.95) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/play.png', confidence=.95))
            sleep(0.05)
            pyautogui.click()

        if pyautogui.locateCenterOnScreen('menu/online.png', confidence=.95) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/online.png', confidence=.95))
            sleep(0.05)
            pyautogui.click()

        if pyautogui.locateCenterOnScreen('menu/okay.png', confidence=.95) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/okay.png', confidence=.95))
            sleep(0.05)
            pyautogui.click()

        if pyautogui.locateCenterOnScreen('menu/find_game.png', confidence=.8) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/find_game.png', confidence=.8))
            sleep(0.05)
            pyautogui.click()


        """
        this is where the imposter/crewmate is set, whenever it sees these
        """
        if pyautogui.locateCenterOnScreen('other/crewmate.png', confidence=.9) != None:
            bot_messages = []
            chat_messages = []
            imposter = False
            print("CREWMATE")

        if pyautogui.locateCenterOnScreen('other/imposter.png', confidence=.9) != None:
            bot_messages = []
            chat_messages = []
            imposter = True
            print("IMPOSTER")
        
        """
        here is the code for finding a lobby with adequate players (>9 in this case), here it goes throughh the regions defined (each of which is a lobby) and reads the playercount, and clicking if the condition is met
        after it will click the 'refresh' button to come up with new lobbies
        """
        if pyautogui.locateCenterOnScreen('menu/find_game1.png', confidence=.8) != None:
            for lobby in [
                (1725, 450),
                (1725, 650),
                (1725, 850),
                (1725, 1050),
                (1725, 1250)
            ]:
                try:
                    pyautogui.screenshot('temp/temp_lobby.png', region=(*lobby, 275, 50))
                    result = reader.readtext("temp/temp_lobby.png")
                    result = "".join([text for (bbox, text, prob) in result])
                    result = int(result[:result.find("/")].strip())
                    print("lobby players:", result)
                    if result > 9:
                        pyautogui.moveTo(*lobby)
                        sleep(0.05)
                        pyautogui.click()
                        sleep(0.05)
                except:
                    pass
            pyautogui.moveTo(1300, 1500) #refresh
            sleep(0.05)
            pyautogui.click()
            sleep(0.1)
            pyautogui.moveTo(*NEUTRAL)

        """
        here is the code for pressing the play again button and continue button, upon pressing the continue button it would adjust the w/l ratio accordingly using the text file
        """
        #press play again button
        if pyautogui.locateCenterOnScreen('menu/again.png', confidence=.8) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/again.png', confidence=.8))
            sleep(0.05)
            pyautogui.click()
            sleep(0.05)
            pyautogui.moveTo(*NEUTRAL)

        #press continue button
        if pyautogui.locateCenterOnScreen('menu/continue.png', confidence=.8) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('menu/continue.png', confidence=.8))
            sleep(0.05)
            with open("stats.txt", "r") as file:
                text = file.readlines()[0].strip()
                
                if pyautogui.locateCenterOnScreen('menu/victory.png', confidence=.8) != None:
                    text += "w"

                if pyautogui.locateCenterOnScreen('menu/defeat.png', confidence=.8) != None:
                    text += "l"
                    
                wr = text.count("w")*100 / len(text)
                print(wr)
                print(text.count("w"), text.count("l")+text.count("w"))

            with open("stats.txt", "w") as file:
                file.write(text+"\n"+str(round(wr, 1))+"%")
            pyautogui.click()  
            sleep(0.05)
            pyautogui.moveTo(*NEUTRAL)
        
        """
        here is the logic for being IN a lobby with players
        it will look at the playercount and click the 'start' button if it is >9
        it will also move around randomly in small bits
        """
        in_lobby = (pyautogui.locateCenterOnScreen('other/lobby.png', confidence=.8) != None)
        if in_lobby:
            try:
                pyautogui.screenshot('temp/temp_lobby.png', region=(2310, 680, 200, 55))
                result = reader.readtext("temp/temp_lobby.png")
                result = "".join([text for (bbox, text, prob) in result])
                result = int(result[:result.find("/")].strip())
                print("players:", result)
                if result > 9:
                    pyautogui.moveTo(1285, 1350)
                    sleep(0.05)
                    pyautogui.click()
                if result < 5:
                    pyautogui.moveTo(2222, 130)
                    sleep(0.05)
                    pyautogui.click()
                    sleep(0.05)
                    pyautogui.moveTo(1280, 1280)
                    sleep(0.05)
                    pyautogui.click()
                    sleep(0.05)
            except Exception as e:
                print(e)

            if moving == True:
                r = random.randint(1,4)
                
                match r:
                    case 1:
                        pyautogui.keyDown(left)
                        sleep(random.random()*random.random())
                        pyautogui.keyUp(left)
                    case 2:
                        pyautogui.keyDown(right)
                        sleep(random.random()*random.random())
                        pyautogui.keyUp(right)
                    case 3:
                        pyautogui.keyDown(up)
                        sleep(random.random()*random.random())
                        pyautogui.keyUp(up)
                    case 4:
                        pyautogui.keyDown(down)
                        sleep(random.random()*random.random())
                        pyautogui.keyUp(down)
            
        else:
            chat_open = (pyautogui.locateCenterOnScreen('other/report.png', confidence=.9) != None)
            
            if pyautogui.locateCenterOnScreen('other/chat.png', confidence=.8) == None and pyautogui.locateCenterOnScreen('other/map.png', confidence=.8) != None and not chat_open:
                if moving == True:
                    """
                    here is the logic for wandering around (moving around the map & doing tasks)
                    it will press e and move in a random direction
                    it will move in all four directions IF the emergency button is not sighted
                    otherwise it will only move in three directions as that means it is in the spawn area
                    """
                    while pyautogui.locateCenterOnScreen('other/chat.png', confidence=.8) == None and pyautogui.locateCenterOnScreen('other/map.png', confidence=.8) != None and not chat_open:
                        
                        if pyautogui.locateCenterOnScreen('other/emergency.png', confidence=.9) == None:
                            r = random.randint(1,4)
                            pyautogui.press('e')
                            match r:
                                case 1:
                                    # pyautogui.keyUp('left')
                                    pyautogui.keyUp(right)
                                    pyautogui.keyDown(left)
                                    if imposter:
                                        pyautogui.press('q')
                                    else:
                                        pyautogui.press('r')
                                case 2:
                                    pyautogui.keyUp('left')
                                    # pyautogui.keyUp(right)
                                    pyautogui.keyDown(right)
                                    if imposter:
                                        pyautogui.press('q')
                                    else:
                                        pyautogui.press('r')
                                case 3:
                                    pyautogui.keyUp(up)
                                    # pyautogui.keyUp(down)
                                    pyautogui.keyDown(down)
                                    if imposter:
                                        pyautogui.press('q')
                                    else:
                                        pyautogui.press('r')
                                case 4:
                                    # pyautogui.keyUp('up')
                                    pyautogui.keyUp(down)
                                    pyautogui.keyDown(up)
                                    if imposter:
                                        pyautogui.press('q')
                                    else:
                                        pyautogui.press('r')
                        else:
                            r = random.randint(1,3)
                            match r:
                                case 1:
                                    pyautogui.keyUp(left)
                                    pyautogui.keyUp(right)
                                    pyautogui.keyDown(left)
                                    pyautogui.press('r')
                                    sleep(2)
                                case 2:
                                    pyautogui.keyUp(left)
                                    pyautogui.keyUp(right)
                                    pyautogui.keyDown(right)
                                    pyautogui.press('r')
                                    sleep(2)
                                case 3:
                                    pyautogui.keyUp(up)
                                    pyautogui.keyUp(down)
                                    pyautogui.keyDown(down)
                                    pyautogui.press('r')
                                    sleep(2)
                        
                        #tasks
                        if random.randint(1,5) == 1:
                            if pyautogui.locateCenterOnScreen('other/emergency_button.png', confidence=.9) != None: #emergency button
                                print("no emergency button")
                                pyautogui.press('escape')
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            'samples' refers to a task in which you have to click a button to dispense 'samples' and after a short wait click the anomaly
                            this is done by first clicking the dispense button,
                            then using certain positions in which the vials will be stored, and checking the color (the bad one will be red)
                            """
                            if pyautogui.locateCenterOnScreen('tasks/samples.png', confidence=.8) != None:
                                print("samples")
                                pyautogui.moveTo(1727, 1389)
                                sleep(1)
                                pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)
                            
                            if pyautogui.locateCenterOnScreen('tasks/samples1.png', confidence=.8) != None:
                                print("samples1") #1252
                                for i in [
                                    (952, 727),
                                    (1118, 727),
                                    (1288, 727),
                                    (1453, 725),
                                    (1624, 722)
                                ]:
                                    if pyautogui.pixel(*i) == (241, 129, 130):
                                        pyautogui.moveTo(i[0], 1252)
                                sleep(0.05)
                                pyautogui.click()
                                sleep(0.05)
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            'asteroids' is a task in which you click on a small screen to shoot asteroids
                            I have found that it is actually faster to randomly click than look for them
                            """
                            if pyautogui.locateCenterOnScreen('tasks/asteroids.png', confidence=.8) != None:
                                print("asteroids")
                                while pyautogui.locateCenterOnScreen('tasks/asteroids.png', confidence=.8) != None:
                                    pyautogui.moveTo(random.randint(700, 1800), random.randint(300, 1300))
                                    sleep(0.05)
                                    pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            calculate distributor is essentially three circles spinning and you have to stop them sequentially when they are pointing the correct way
                            this is done by looking at the bar next to them which will light up when it is at the correct orientation
                            """
                            if pyautogui.locateCenterOnScreen('tasks/calibrate_distributor.png', confidence=.9) != None:
                                print("calibrate_distributor")
                                while pyautogui.pixel(1740, 340) == (0, 0, 0):
                                    pass
                                pyautogui.moveTo(1680, 460) #yellow
                                sleep(0.05)
                                pyautogui.click()
                                while pyautogui.pixel(1740, 740) == (0, 0, 0):
                                    pass
                                pyautogui.moveTo(1680, 860) #blue
                                sleep(0.05)
                                pyautogui.click()
                                while pyautogui.pixel(1740, 1130) == (0, 0, 0):
                                    pass
                                pyautogui.moveTo(1680, 1260) #light blue
                                sleep(0.05)
                                pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            empty chute is simple, there is a lever that empties it
                            """
                            if pyautogui.locateCenterOnScreen('tasks/empty_chute.png', confidence=.9) != None:
                                print("empty_chute")
                                pyautogui.moveTo(1745, 620)
                                sleep(0.05)
                                pyautogui.mouseDown()
                                pyautogui.move(0, 500, 0.5)
                                sleep(5)
                                pyautogui.mouseUp()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            'stabilise steering' you click in the middle thats it
                            """
                            if pyautogui.locateCenterOnScreen('tasks/stabilise.png', confidence=.95) != None:
                                print("stabilise")
                                pyautogui.moveTo(1280, 800)
                                sleep(0.05)
                                pyautogui.click()
                                sleep(0.05)
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            in this aligning task you have to drag a pointer down to the middle
                            I found it was easier to drag from random spots as finding out exactly where it is is difficult as it is angled
                            """
                            if pyautogui.locateCenterOnScreen('tasks/align.png') != None:
                                print("align")
                                while pyautogui.locateCenterOnScreen('tasks/align.png') != None:
                                    pyautogui.moveTo(1776, random.randint(216, 1373))
                                    pyautogui.mouseDown()
                                    sleep(0.05)
                                    pyautogui.moveTo(1776, 800, 0.2)
                                    sleep(0.01)
                                    pyautogui.mouseUp()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            the 'divert' tasks are split into two parts
                            part one:
                            you click the middle to allow power to go through
                            part two:
                            you drag a slider up to allow the power to go through
                            """
                            if pyautogui.locateCenterOnScreen('tasks/divert1.png', confidence=.8) != None:
                                print("divert1")
                                pyautogui.moveTo(pyautogui.locateCenterOnScreen('tasks/divert1.png', confidence=.8))
                                sleep(0.05)
                                pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

                            if pyautogui.locateCenterOnScreen('tasks/divert.png', confidence=.8) != None:
                                print("divert")
                                pyautogui.moveTo(pyautogui.locateCenterOnScreen('tasks/divert.png', confidence=.8))
                                sleep(0.05)
                                pyautogui.mouseDown()
                                pyautogui.move(0, -500, 0.5)
                                pyautogui.mouseUp()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            the 'wires' task includes dragging colored wires from one side to the other, matching colors
                            this is done using two lists of wire 'positions' on either side, and appending the color to their respective side list
                            then the wire from the left is dragged to the right
                            """
                            if pyautogui.locateCenterOnScreen('tasks/wires.png', confidence=.8) != None:
                                print("wires")
                                left, right = [], []
                                left_positions = [(690, 400), (690, 680), (690, 960), (690, 1220)]
                                right_positions = [(1850, 400), (1850, 680), (1850, 960), (1850, 1220)]
                                for i in left_positions:
                                    left.append(pyautogui.pixel(*i))
                                for i in right_positions:
                                    right.append(pyautogui.pixel(*i))
                                
                                for i in range(4):
                                    pyautogui.moveTo(left_positions[i])
                                    pyautogui.mouseDown()
                                    pyautogui.moveTo(*right_positions[right.index(left[i])], 0.5)
                                    pyautogui.mouseUp()
                                pyautogui.moveTo(*NEUTRAL)
                                
                            """
                            the download and upload tasks you click the download and upload button
                            """
                            if pyautogui.locateCenterOnScreen('tasks/download.png', confidence=.8) != None:
                                print("download")
                                pyautogui.moveTo(pyautogui.locateCenterOnScreen('tasks/download.png', confidence=.8))
                                sleep(0.05)
                                pyautogui.click()
                                sleep(0.05)
                                pyautogui.moveTo(*NEUTRAL)

                            if pyautogui.locateCenterOnScreen('tasks/upload.png', confidence=.8) != None:
                                print("upload")
                                pyautogui.moveTo(pyautogui.locateCenterOnScreen('tasks/upload.png', confidence=.8))
                                sleep(0.05)
                                pyautogui.click()
                                sleep(0.05)
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            in the clean vent task, you have to click objects in the vent to 'clean' them (they disappear), this is done with more random clicking in the vent area
                            """
                            if pyautogui.locateCenterOnScreen('tasks/clean_vent.png', confidence=.8) != None:
                                print("clean vent")
                                pyautogui.moveTo(random.randint(559, 2074), random.randint(282, 1376))
                                pyautogui.click()
                                sleep(0.5)
                                while pyautogui.locateCenterOnScreen('tasks/clean_vent1.png', confidence=.8) != None:
                                    pyautogui.moveTo(random.randint(559, 2074), random.randint(282, 1376))
                                    pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            simon says is a game in which there are two panels:
                            the panel on the left will display a pattern of flashes that you have to memorise, each phase a new square is added to the pattern
                            the panel on the right has input in which you mimic the pattern flashed on the left

                            to solve this, i used a list of locations on the left and looked at them until one of them changed to the color of being on, adding it to a list for future reference
                            i checked this until the number of flashes was equal to the phase we were at
                            then input the pattern on the right side using another list of locations
                            """
                            if pyautogui.locateCenterOnScreen('tasks/simon.png', confidence=.8) != None:
                                print("simon")
                                simon_locations = [
                                    (642, 700),
                                    (823, 700),
                                    (1020, 700),
                                    (642, 860),
                                    (823, 860),
                                    (1020, 860),
                                    (642, 1050),
                                    (823, 1050),
                                    (1020, 1050)
                                ]
                                simon_button_locations = [
                                    (1540, 700),
                                    (1728, 700),
                                    (1900, 700),
                                    (1540, 800),
                                    (1728, 800),
                                    (1900, 800),
                                    (1540, 1060),
                                    (1728, 1060),
                                    (1900, 1060)
                                ]
                                pattern = []
                                for n in range(1, 11):
                                    pattern = []
                                    for j in range(n):
                                        lit_up = None
                                        while lit_up == None:
                                            for i in range(len(simon_locations)):
                                                if pyautogui.pixel(*simon_locations[i]) == (68, 168, 255):
                                                    lit_up = i
                                                    pattern.append(i)
                                        while pyautogui.pixel(*simon_locations[lit_up]) == (68, 168, 255):
                                            pass

                                    for i in pattern:
                                        pyautogui.moveTo(simon_button_locations[i])
                                        sleep(0.05)
                                        pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            card swipe is a task in which you have to drag a card left to right
                            first, we have to click the card to bring it up to the reader
                            then we have to hold down on the card
                            then we drag it across using moveTo and let go, completing the swipe
                            """
                            if pyautogui.locateCenterOnScreen('tasks/card.png', confidence=.8) != None:
                                print("card swipe")
                                pyautogui.moveTo(1084, 1217)
                                sleep(0.05)
                                pyautogui.click()
                                sleep(1)
                                pyautogui.moveTo(639, 620)
                                pyautogui.mouseDown()
                                # pyautogui.dragTo(3000, 620, 1.5, button='left')
                                pyautogui.moveTo(2500, 620, 1.5)
                                pyautogui.mouseUp()
                                pyautogui.moveTo(*NEUTRAL)

                            """
                            the shields task is one in which you have to click red shield icons until they are all white
                            however clicking a white shield icon will turn it red
                            due to this it will be hard to tell if it is red as the shield icons are transparent and the background will heavily affect the color
                            resorted to using random clicks
                            """
                            if pyautogui.locateCenterOnScreen('tasks/shields.png', confidence=.8) != None:
                                print("shields")
                                shield_positions = [
                                    (1281, 427),
                                    (996, 586),
                                    (1295, 819),
                                    (1555, 616),
                                    (1561, 971),
                                    (1268, 1118),
                                    (960, 978)
                                ]
                                while pyautogui.locateCenterOnScreen('tasks/shields.png', confidence=.8) != None:
                                    pyautogui.moveTo(shield_positions[random.randint(0,len(shield_positions)-1)])
                                    pyautogui.click()
                                pyautogui.moveTo(*NEUTRAL)

        in_meeting = (pyautogui.locateCenterOnScreen('other/meeting.png') != None)
        if in_meeting:
            if pyautogui.locateCenterOnScreen('other/chat.png', confidence=.9) != None and pyautogui.locateCenterOnScreen('other/dead.png', confidence=.95 == None):
                """
                this will open chat so the bot can use it
                """
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
                chat_button_location = pyautogui.locateCenterOnScreen('other/chat.png')
                pyautogui.moveTo(chat_button_location)
                sleep(0.1)
                pyautogui.click()
                sleep(0.1)
                pyautogui.moveTo(*NEUTRAL)
                sleep(5)
            try:
                """
                this is where it sends a chat message
                first it takes a screenshot of the chat and saves it to temp.png
                then it 'purifies' the image, making all non black or close colors white, so the text is clearly highlighted
                we then use ocr to read the text in the image and save it to result

                we set messages to just the prompt message (loaded in a txt)
                we append the information list to the messages list
                we append the examples to the messages list (from txt)
                we then append the chat messages, making sure to tell it that it is not exact and only an approximation
                we also add it to the list chat_messages for further use
                we then give it what the bot itself has said so far

                then, it is generated, with some adjustments such as removing punctuation to make it seem more 'human'
                we then log the message sent and then type it out, and send it in chat
                """
                #chatting
                messages = [{"role": "system", "content": open("prompt_message.txt", "r").read()}]
                # im = pyscreeze.screenshot(region=(500, 150, 1250, 845))
                # im.save("temp.png")
                pyautogui.screenshot('temp/temp.png', region=(636, 63, 1102, 986))
                img = np.array(Image.open('temp/temp.png'))
                # Set range of color values
                lower = np.array([50, 50, 50])
                upper = np.array([255, 255, 255])
                # Threshold the image to get only selected colors
                mask = cv.inRange(img, lower, upper)
                # Set the new value to the masked image
                img[mask.astype(bool)] = 255
                Image.fromarray(img).save("temp/temp.png")
                result = reader.readtext("temp/temp.png")
                # messages = pytesseract.image_to_string('temp.png')
                messages.append({"role": "system", "content": "information gathered in the round will be provided in the next message."})
                messages.append({"role": "system", "content": "\n".join(information)})

                messages.append({"role": "system", "content": "examples will be provided in the next message, where [CREW] is a crewmate (referred to by color) and should be replaced."})
                messages.append({"role": "system", "content": "\n".join(open("chat_examples.txt", "r").readlines())})
                
                messages.append({"role": "system", "content": "an approximation of chat will be provided in the next few messages, with names preceding the message. messages saying someone has voted are not sent by anyone but the game."})
                for (bbox, text, prob) in result:
                    # print(text)
                    # if not any(i == text for i in chat_messages):
                    # messages.append({"role": "user", "content": text})
                    chat_messages.append(text)
                
                if len(chat_messages) > 0:
                    for message in chat_messages:
                        messages.append({"role": "user", "content": message})

                if len(bot_messages) > 0:
                    messages.append({"role": "system", "content": "here is what you have said so far, NOT including other messages/responses to yours. remember to consider chat messages from other people."})
                    for text in bot_messages:
                        messages.append({"role": "assistant", "content": text})
                pyautogui.press('a')
                response = ollama.chat(
                    model=model,  # Replace with the name of your loaded model
                    messages=messages,
                    options={
                        "temperature": 0.9
                    },
                )['message']['content']
                print(response)
                response = response.lower().replace("waddleking","").replace("suspicious","sus").replace(".","").replace("!","").replace(":","").replace("'","").strip()
                response = re.sub("[\(\[].*?[\)\]]", "", response)
                if response.count("\n") > 0:
                    response = response[:response.find("\n")]
                bot_messages.append(response)
                pyautogui.press('backspace')
                print(response)
                with open("log.txt", "a") as file:
                    file.write("\n"+response)
                pyautogui.press('backspace')
                pyautogui.write(response, interval=0.05)
                pyautogui.press('enter')
                for i in range(random.randint(5,15)):
                    voting_phase = (pyautogui.locateCenterOnScreen('other/begin.png') == None)
                    if voting_phase:
                        """
                        here is the voting (also using llm)
                        first we check if its actually time to vote (reading whats displayed in the bottom right timer)

                        we then follow the same process as before, taking a screenshot and bleaching out all the non black or close colors to get just the text from the chat
                        we set messages to the prompt message for voting, loaded from txt
                        we give it the chat messages which have been said during the whole round
                        and we give it the colors availible to choose from (players)
                        we then generate a response, saved in response
                        
                        we see if it is 'skip' or a valid color
                        if it is, we will try and find that color on the screen and vote them
                        or just click the skip vote button
                        if not, we will vote someone random
                        """
                        try:
                            pyautogui.screenshot('temp/temp_time.png', region=(2194, 1333, 139, 45))
                            result = reader.readtext("temp/temp_time.png")
                            result = float("".join([text for (bbox, text, prob) in result]).replace("s","").replace(":","").strip())
                            if result > 32:
                                sleep(1)
                            else:
                                try:
                                    pyautogui.screenshot('temp/temp.png', region=(636, 63, 1102, 986))
                                    img = np.array(Image.open('temp/temp.png'))
                                    # Set range of color values
                                    lower = np.array([50, 50, 50])
                                    upper = np.array([255, 255, 255])
                                    # Threshold the image to get only selected colors
                                    mask = cv.inRange(img, lower, upper)
                                    # Set the new value to the masked image
                                    img[mask.astype(bool)] = 255
                                    Image.fromarray(img).save("temp/temp.png")
                                    result = reader.readtext("temp/temp.png")
                                    for (bbox, text, prob) in result:
                                        chat_messages.append(text)
                                    pyautogui.moveTo(2040, 1343)
                                    sleep(0.1)
                                    pyautogui.click()
                                    #voting
                                    try:
                                        print("\n".join(chat_messages))
                                        messages = [{"role": "system", "content": open("prompt_vote.txt", "r").read()}]
                                        if len(bot_messages) > 0:
                                            messages.append({"role": "system", "content": "here is what you have said so far, NOT including other messages/responses to yours."})
                                            messages.append({"role": "system", "content": "\n".join(bot_messages)})
                                        if len(chat_messages) > 0:
                                            messages.append({"role": "system", "content": "here is an approximation of what has been said in chat for the previous rounds, with usernames preceding the message. Messages saying someone has voted are not sent by anyone but the game."})
                                            messages.append({"role": "system", "content": "\n".join(chat_messages)})
                                        messages.append({"role": "system", "content": "here are the colors you can choose from:"})
                                        messages.append({"role": "system", "content": ", ".join(colors)})
                                        response = ollama.chat(
                                            model=model,  # Replace with the name of your loaded model
                                            messages=messages,
                                            options={
                                                "temperature": 0.9
                                            },
                                        )['message']['content'].replace(".","").strip().lower()
                                        print("CHOICE:",response)
                                        if response == "skip":
                                            pyautogui.moveTo(453, 1345)
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.1)
                                            pyautogui.moveTo(659, 1345)
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.5)
                                        else:
                                            pyautogui.moveTo(pyautogui.locateCenterOnScreen(f'colors/{response}.png', confidence=.95))
                                            pyautogui.move(0, -10)
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.5)
                                        print("VOTED FOR:",response)
                                    except Exception as e:
                                        print(e)
                                    #click random things
                                    for i in range(25):
                                        in_meeting = (pyautogui.locateCenterOnScreen('other/meeting.png', confidence=.9) != None)
                                        if in_meeting:
                                            r = random.randint(0, len(possible_votes)-1)
                                            pyautogui.moveTo(possible_votes[r][0], possible_votes[r][1])
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.1)
                                            pyautogui.moveTo(659, 1345)
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.1)
                                except:
                                    print("a")
                        except:
                            pass
                    else:
                        sleep(0.05)
            except Exception as e:
                print(e)
                