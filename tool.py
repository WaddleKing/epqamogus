import pyautogui, pyscreeze, keyboard
from time import sleep

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

    print("started")
    while True:

        if keyboard.is_pressed("control"):
            try:
                point = pyautogui.position()
                im = pyscreeze.screenshot()
                
                print(point)
                #print(im.getpixel((pyautogui.position().x, pyautogui.position().y)))
                while keyboard.is_pressed("control"):
                    pass
            except IndexError:
                print()

        sleep(0.05)
