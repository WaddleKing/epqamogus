import pyautogui, pyscreeze, keyboard
from time import sleep
import easyocr
import ollama
import subprocess
import random
# import pytesseract

def click(x, y, duration=0.1):
    pyautogui.click(
        x,
        y,
        duration=duration
    )


def getColor(x, y):
    im = pyscreeze.screenshot()
    return im.getpixel((x,y))


def checkColor(x, y, color):
    return tolerance(color, getColor(x, y))


def tolerance(color, scolor, tolerance=15):
    r, g, b = color[:3]
    exR, exG, exB = scolor
    return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance)

def do_task():
    pass

if __name__ == "__main__":
    reader = easyocr.Reader(['en'])

    screen_height, screen_width = 2560, 1600

    pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False
    pyautogui.FAILSAFE = False

    # pyautogui.screenshot('report.png', region=(2003, 757, 129, 80))
    # pyautogui.screenshot('lobby.png', region=(2405, 104, 45, 53))
    # pyautogui.screenshot('meeting.png', region=(2405, 104, 45, 53))
    information = []
    bot_messages = []

    model = "hf.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF:Q8_0"

    subprocess.Popen(["ollama", "serve"])
    subprocess.Popen(["ollama", "pull", model])

    # pytesseract.pytesseract.tesseract_cmd = "C:/Users/jesus/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

    game_state = None
    colors = ["Red", "Blue", "Green", "Pink", "Orange", "Yellow", "Black", "White", "Purple", "Brown", "Cyan", "Lime", "Maroon", "Rose", "Banana", "Gray", "Tan", "Coral", "skip"]
    possible_votes = [(655, 410), (1377, 410), (2116, 410), 
                      (655, 610), (1377, 610), (2116, 610), 
                      (655, 800), (1377, 800), (2116, 800), 
                      (655, 970), (1377, 970), (2116, 970), 
                      (655, 1165), (1377, 1165), (2116, 1165),
                      (453, 1345), (659, 1345)]
    print("started")
    while True:
        #press play again button
        if pyautogui.locateCenterOnScreen('other/again.png', confidence=.8) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('other/again.png', confidence=.8))
            sleep(0.1)
            pyautogui.click()
            bot_messages = []

        #press continue button
        if pyautogui.locateCenterOnScreen('other/continue.png', confidence=.8) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen('other/continue.png', confidence=.8))
            sleep(0.1)
            pyautogui.click()

        in_lobby = (pyautogui.locateCenterOnScreen('other/lobby.png', confidence=.8) != None)
        if in_lobby:
            r = random.randint(1,4)
            match r:
                case 1:
                    pyautogui.keyDown('left')
                    sleep(random.random()*random.random())
                    pyautogui.keyUp('left')
                case 2:
                    pyautogui.keyDown('right')
                    sleep(random.random()*random.random())
                    pyautogui.keyUp('right')
                case 3:
                    pyautogui.keyDown('up')
                    sleep(random.random()*random.random())
                    pyautogui.keyUp('up')
                case 4:
                    pyautogui.keyDown('down')
                    sleep(random.random()*random.random())
                    pyautogui.keyUp('down')
        else:
            chat_open = (pyautogui.locateCenterOnScreen('other/report.png', confidence=.9) != None)
            
                
            if pyautogui.locateCenterOnScreen('other/chat.png', confidence=.9) == None and pyautogui.locateCenterOnScreen('other/map.png', confidence=.9) != None and not chat_open:
                #wandering around
                r = random.randint(1,4)
                match r:
                    case 1:
                        pyautogui.keyUp('right')
                        pyautogui.keyDown('left')
                    case 2:
                        pyautogui.keyUp('up')
                        pyautogui.keyDown('down')
                    case 3:
                        pyautogui.keyUp('left')
                        pyautogui.keyDown('right')
                    case 4:
                        pyautogui.keyUp('down')
                        pyautogui.keyDown('up')
                    case 5:
                        pyautogui.keyUp('right')
                    case 6:
                        pyautogui.keyUp('up')
                    case 7:
                        pyautogui.keyUp('left')
                    case 8:
                        pyautogui.keyUp('down')

        tabbed_in = checkColor(1277, 61, (170, 187, 187))


        in_meeting = (pyautogui.locateCenterOnScreen('other/meeting.png', confidence=.95) != None)
        if in_meeting:
            if pyautogui.locateCenterOnScreen('other/chat.png', confidence=.9) != None and pyautogui.locateCenterOnScreen('other/dead.png', confidence=.95 == None):
                pyautogui.keyUp('left')
                pyautogui.keyUp('right')
                pyautogui.keyUp('up')
                pyautogui.keyUp('down')
                chat_button_location = pyautogui.locateCenterOnScreen('other/chat.png')
                pyautogui.moveTo(chat_button_location)
                sleep(0.1)
                pyautogui.click()
                sleep(0.1)
                pyautogui.moveTo(1000, 1000)
                sleep(5)
            try:
                
                #chatting
                messages = [{"role": "system", "content": open("prompt_message.txt", "r").read()}]
                # im = pyscreeze.screenshot(region=(500, 150, 1250, 845))
                # im.save("temp.png")
                pyautogui.screenshot('temp.png', region=(636, 63, 1102, 986))
                result = reader.readtext("temp.png")
                # messages = pytesseract.image_to_string('temp.png')
                messages.append({"role": "system", "content": "information gathered in the round will be provided in the next message."})
                messages.append({"role": "system", "content": "\n".join(information)})

                messages.append({"role": "system", "content": "examples will be provided in the next message, where [CREW] is a crewmate (referred to by color)."})
                messages.append({"role": "system", "content": "\n".join(open("chat_examples.txt", "r").readlines())})
                
                messages.append({"role": "system", "content": "an approximation of chat will be provided in the next few messages, with names preceding the message."})
                for (bbox, text, prob) in result:
                    # print(text)
                    messages.append({"role": "user", "content": text})

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
                )['message']['content'].lower().replace("waddleking:","").replace("suspicious:","sus").replace(".","").replace("!","").replace("'","").strip()
                if response.count("\n") > 0:
                    response = response[:response.find("\n")]
                bot_messages.append(response)
                print(response)
                pyautogui.press('backspace')
                pyautogui.write(response, interval=0.05)
                pyautogui.press('enter')
                for i in range(random.randint(5,15)):
                    print(i)
                    voting_phase = (pyautogui.locateCenterOnScreen('other/begin.png') == None)
                    print(voting_phase)
                    if voting_phase:
                        try:
                            pyautogui.screenshot('temp_time.png', region=(2194, 1333, 139, 45))
                            result = reader.readtext("temp_time.png")
                            result = float("".join([text for (bbox, text, prob) in result]).replace("s","").replace(":","").strip())
                            print(result)
                            if result > 20:
                                sleep(1)
                            else:
                                try:
                                    pyautogui.moveTo(2040, 1343)
                                    sleep(0.1)
                                    pyautogui.click()
                                    #voting
                                    try:
                                        messages = [{"role": "system", "content": open("prompt_vote.txt", "r").read()}]
                                        if len(bot_messages) > 0:
                                            messages.append({"role": "system", "content": "here is what you have said so far, NOT including other messages/responses to yours."})
                                            messages.append({"role": "system", "content": "\n".join(bot_messages)})
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
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.1)
                                            pyautogui.moveTo(659, 1345)
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.5)
                                        else:
                                            pyautogui.moveTo(pyautogui.locateCenterOnScreen(f'colors/{response}.png', confidence=.95))
                                            pyautogui.move(0, -10)
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.3)
                                            pyautogui.click()
                                            sleep(0.5)
                                        print("VOTED FOR:",response)
                                    except:
                                        print()
                                    #click random things
                                    for i in range(25):
                                        in_meeting = (pyautogui.locateCenterOnScreen('other/meeting.png', confidence=.9) != None)
                                        if in_meeting:
                                            r = random.randint(0, len(possible_votes)-1)
                                            pyautogui.moveTo(possible_votes[r][0], possible_votes[r][1])
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.1)
                                            pyautogui.moveTo(659, 1345)
                                            sleep(0.1)
                                            pyautogui.click()
                                            sleep(0.1)
                                except:
                                    print()
                        except:
                            pass
                    else:
                        sleep(1)
            except:
                print()
                

        # sleep(0)

        if tabbed_in:
            game_state = "a"
        else:
            game_state = None