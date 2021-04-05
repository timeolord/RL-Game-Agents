import os
import time
import gym
import numpy as np
import win32api
import win32con
import win32gui
from gym import spaces
from pytesseract import pytesseract
import mss
import mss.tools
import cv2
from stable_baselines.common.env_checker import check_env
import re
import matplotlib.pyplot as plt
from ReadWriteMemory import ReadWriteMemory

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

VK_CODE = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE,
           '`': 0xC0}


def selectHero(heroX, heroY):
    click(heroX, heroY)
    click(heroX, heroY)


def click(mouseX, mouseY):
    win32api.SetCursorPos((mouseX, mouseY))
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mouseX, mouseY, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mouseX, mouseY, 0, 0)
    time.sleep(1.5)


def press(char):
    win32api.keybd_event(VK_CODE[char], 0, 0, 0)
    time.sleep(.1)
    win32api.keybd_event(VK_CODE[char], 0, win32con.KEYEVENTF_KEYUP, 0)


def screenshot(screenX, screenY, width, height, reduction_factor=1, gray=True):
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': screenX, 'top': screenY, 'width': width, 'height': height}

        # Grab the data
        img = sct.grab(region)

        if gray:
            result = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2GRAY)
        else:
            result = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

        img = result[::reduction_factor, ::reduction_factor]
        return img


def getDamageDone(threshold=190, var=10):
    done = False

    while not done:

        img = screenshot(-1332, 440, 34, 13, gray=False)

        for rows in range(0, len(img)):
            for cols in range(0, len(img[0])):
                x = img[rows][cols]
                if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                    img[rows][cols] = [0, 0, 0]
                else:
                    img[rows][cols] = [255, 255, 255]

        score = pytesseract.image_to_string(img, lang='eng',
                                            config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

        # plt.imshow(img)
        # plt.show()

        # print(score)

        score = re.sub("[^0-9]", "", score)

        if score != "":
            score = int(score)
            return score


def getDamageTaken(threshold=190, var=10):
    done = False

    while not done:

        img = screenshot(-1316, 450, 18, 12, gray=False)

        for rows in range(0, len(img)):
            for cols in range(0, len(img[0])):
                x = img[rows][cols]
                if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                    img[rows][cols] = [0, 0, 0]
                else:
                    img[rows][cols] = [255, 255, 255]

        score = pytesseract.image_to_string(img, lang='eng')

        # plt.imshow(img)
        # plt.show()

        # print(score)
        score = re.sub("[^0-9]", "", score)

        if score != "":
            score = int(score)
            return score

    '''
    rwm = ReadWriteMemory()

    process = rwm.get_process_by_name('Brawlhalla.exe')
    process.open()

    print(process.__dict__)
    '''


def getKOs(threshold=190, var=10):
    done = False

    while not done:

        img = screenshot(-1309, 408, 11, 13, gray=False)

        for rows in range(0, len(img)):
            for cols in range(0, len(img[0])):
                x = img[rows][cols]
                if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                    img[rows][cols] = [0, 0, 0]
                else:
                    img[rows][cols] = [255, 255, 255]

        score = pytesseract.image_to_string(img, lang='eng',
                                            config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')

        # plt.imshow(img)
        # plt.show()

        # (score)

        score = re.sub("[^0-9]", "", score)

        if score != "":
            score = int(score)
            return score


def isDead(threshold=190, var=10):
    img = screenshot(screenX=-1383, screenY=82, width=44, height=20, gray=False)

    for rows in range(0, len(img)):
        for cols in range(0, len(img[0])):
            x = img[rows][cols]
            if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                img[rows][cols] = [0, 0, 0]
            else:
                img[rows][cols] = [255, 255, 255]

    nextString = pytesseract.image_to_string(img)

    #print(nextString)

    if nextString[0] == "N" or nextString[0] == "n":
        return True
    else:
        return False


def isMenu(threshold=190, var=10):
    img = screenshot(screenX=-1502, screenY=415, width=131, height=26, gray=False)

    for rows in range(0, len(img)):
        for cols in range(0, len(img[0])):
            x = img[rows][cols]
            if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                img[rows][cols] = [0, 0, 0]
            else:
                img[rows][cols] = [255, 255, 255]

    nextString = pytesseract.image_to_string(img)

    # print(nextString)

    if nextString[0] == "L":
        return True
    else:
        return False


def isWin(threshold=190, var=10):
    img = screenshot(screenX=-1572, screenY=314, width=65, height=15, gray=False)

    for rows in range(0, len(img)):
        for cols in range(0, len(img[0])):
            x = img[rows][cols]
            if x[0] > threshold and x[1] > threshold and x[2] > threshold and max(x) - min(x) < var:
                img[rows][cols] = [0, 0, 0]
            else:
                img[rows][cols] = [255, 255, 255]

    nextString = pytesseract.image_to_string(img)

    # print(nextString)

    if nextString[0] == "O":
        return True
    else:
        return False


class brawlhalla_env(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        windowHandle = win32gui.FindWindowEx(None, None, None, "Brawlhalla")
        if windowHandle != 0:
            print("Found")
        else:
            os.startfile(r'D:\Steam Games\steamapps\common\Brawlhalla\Brawlhalla.exe')
            time.sleep(120)

        self.screenWidth = 1080
        self.screenHeight = 1920
        self.resolutionDivider = 2
        self.channels = 1
        self.heroX = -1678
        self.heroY = 108

        windowHandle = win32gui.FindWindowEx(None, None, None, "Brawlhalla")
        if windowHandle != 0:
            print("Found")

        win32gui.MoveWindow(windowHandle, -self.screenHeight - 8, 0, self.screenHeight // self.resolutionDivider,
                            self.screenWidth // self.resolutionDivider, True)
        numberOfActions = 8
        self.action_space = spaces.Discrete(numberOfActions)

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.screenWidth // self.resolutionDivider,
                                                                    self.screenHeight // self.resolutionDivider),
                                            dtype=np.uint8)
        # Starts a game
        click(-1850, 277)
        click(-1608, 282)
        click(-1578, 285)
        click(-1879, 157)
        selectHero(self.heroX, self.heroY)
        press('c')
        time.sleep(1.5)
        click(-1649, 127)

    def reset(self):
        done = False
        print("Resetting")
        dead = isDead()
        if not dead:
            # Exits current game and starts a new game
            click(-1649, 127)
            while not isMenu():
                press('esc')
                time.sleep(1)
            time.sleep(1.5)
            click(-1430, 439)
            time.sleep(10)
            selectHero(self.heroX, self.heroY)
            press('c')
            time.sleep(1.5)
            click(-1649, 127)
            time.sleep(5)
        else:
            selectHero(self.heroX, self.heroY)
            selectHero(self.heroX, self.heroY)
            press('c')
            press('c')
            time.sleep(4)
            press('c')
            press('c')
            time.sleep(4)
            print("selecting hero")
            selectHero(self.heroX, self.heroY)
            selectHero(self.heroX, self.heroY)
            press('c')
            time.sleep(1.5)
            click(-1649, 127)
            time.sleep(5)

        return screenshot(-self.screenHeight, 0, self.screenHeight // self.resolutionDivider,
                          self.screenWidth // self.resolutionDivider)

    def step(self, action):

        #print("Action")

        image = screenshot(-self.screenHeight - 15, 0, self.screenHeight // self.resolutionDivider,
                           self.screenWidth // self.resolutionDivider)

        if action == 0:
            press('up_arrow')
        elif action == 1:
            press('down_arrow')
        elif action == 2:
            press('left_arrow')
        elif action == 3:
            press('right_arrow')
        elif action == 4:
            press('z')
        elif action == 5:
            press('x')
        elif action == 6:
            press('c')
        elif action == 7:
            press('v')

        reward = 0

        done = isDead()

        if done:
            win = isWin()
            if win:
                reward += 1
        else:
            reward = 0.001

        info = {}

        # plt.imshow(image)
        # plt.show()

        return image, reward, done, info

    def render(self, mode='console'):
        pass

    def close(self):
        pass

# print(getKOs())
# getDamageDone()
# getDamageTaken()

# while True:
# x, y = win32api.GetCursorPos()
# print(x, y)
