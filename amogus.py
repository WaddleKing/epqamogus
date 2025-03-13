import pyautogui, pyscreeze, keyboard
from time import sleep

screen_height, screen_width = 1920, 1080

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

game_state = None
colours = ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan", "lime", "maroon", "rose", "banana", "gray", "tan", "coral"]
while True:
    tabbed_in = checkColor(1724, 61, (176, 177, 181))
    if keyboard.is_pressed("control"):
        try:
            point = pyautogui.position()
            im = pyscreeze.screenshot()
            print(point)
            print(im.getpixel((pyautogui.position().x, pyautogui.position().y)))
        except IndexError:
            print()
        sleep(1)

    if tabbed_in:
        pass
    else:
        game_state = None