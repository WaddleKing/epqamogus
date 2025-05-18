import pyautogui, pyscreeze, keyboard
from time import sleep
from PIL import Image
import easyocr
import cv2 as cv
import numpy as np

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

    screen_height, screen_width = 2560, 1600

    pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False

    # pyautogui.screenshot('report.png', region=(2003, 757, 129, 80))
    # pyautogui.screenshot('lobby.png', region=(2405, 104, 45, 53))
    # pyautogui.screenshot('meeting.png', region=(1014, 201, 647, 74))
    # pyautogui.screenshot('meeting.png', region=(218, 189, 98, 88))
    sleep(1)
    # pyautogui.screenshot('time.png', region=(1816, 1317, 541, 89))
    pyautogui.screenshot("screen.png")
    # reader = easyocr.Reader(['en'])
    # result = reader.readtext("manifolds.png")
    # result = "".join([text for (bbox, text, prob) in result])
    # print(result)
    # pyautogui.screenshot('temp.png', region=(636, 63, 1102, 986))
    # img = np.array(Image.open('temp.png'))
    # # Set range of color values
    # lower = np.array([30, 30, 30])
    # upper = np.array([255, 255, 255])
    # # Threshold the image to get only selected colors
    # mask = cv.inRange(img, lower, upper)
    # # Set the new value to the masked image
    # img[mask.astype(bool)] = 255
    # Image.fromarray(img).save("temp.png")

    print("started")
    while True:

        if keyboard.is_pressed("control"):
            try:
                point = pyautogui.position()
                im = pyscreeze.screenshot()
                
                print(point)
                #print(im.getpixel((pyautogui.position().x, pyautogui.position().y)))
                print(pyautogui.pixel(*point))
                while keyboard.is_pressed("control"):
                    pass
            except IndexError:
                print()

        sleep(0.05)
