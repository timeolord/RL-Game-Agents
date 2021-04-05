import os
import time
from ctypes import wintypes
import pyautogui
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
import re
import matplotlib.pyplot as plt
from ReadWriteMemory import ReadWriteMemory
import math
import ctypes
from ctypes import *
import psutil
import pymem
import keyboard

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

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             LPINPUT,  # pInputs
                             ctypes.c_int)  # cbSize

PUL = ctypes.POINTER(ctypes.c_ulong)


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def setMousePos(x, y):
    x = 1 + int(x * 65536. / 1920.)
    y = 1 + int(y * 65536. / 1080.)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def click(mouseX, mouseY):
    win32api.SetCursorPos((mouseX, mouseY))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mouseX, mouseY, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mouseX, mouseY, 0, 0)


def rightClick(mouseX, mouseY):
    win32api.SetCursorPos((mouseX, mouseY))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, mouseX, mouseY, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, mouseX, mouseY, 0, 0)


def press(char):
    PressKey(VK_CODE[char])
    time.sleep(0.2)
    ReleaseKey(VK_CODE[char])


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


def mainMenuToAct1():
    # Enters mission select
    press('enter')
    time.sleep(3)
    # Enters act 1
    press('d')
    press('enter')
    time.sleep(1)
    press('enter')
    time.sleep(0.5)
    # Skips intro
    press('a')
    time.sleep(0.5)
    press('enter')
    time.sleep(7)
    # Selects first mask
    press('enter')


def suicide():
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    press('w')
    time.sleep(2)
    press('r')
    press('r')
    press('r')
    press('r')
    press('r')
    press('r')
    press('r')


class hotlinemiami_env(gym.Env):

    def __init__(self):
        windowHandle = win32gui.FindWindowEx(None, None, None, "Hotline Miami 2: Wrong Number")
        if windowHandle != 0:
            print("Found")
        else:
            os.startfile(r'D:\Steam Games\steamapps\common\Hotline Miami 2\HotlineMiami2.exe')
            time.sleep(10)
            windowHandle = win32gui.FindWindowEx(None, None, None, "Hotline Miami 2: Wrong Number")
            if windowHandle != 0:
                print("Found")

        base = 0x00930000
        offset = 0x00297030
        self.pointerStatic = base + offset

        self.rwm = ReadWriteMemory()
        self.process = self.rwm.get_process_by_name("HotlineMiami2.exe")
        self.process.open()
        print(self.process.__dict__)

        self.screenWidth = 1080
        self.screenHeight = 1920
        self.resolutionDivider = 2
        self.actualWidth = self.screenWidth // self.resolutionDivider
        self.actualHeight = self.screenHeight // self.resolutionDivider
        self.relativePosX = -self.screenHeight - 8
        self.relativePosY = 0
        self.windowCenterX = self.relativePosX + 8 + self.actualHeight // 2
        self.windowCenterY = self.relativePosY + self.actualWidth // 2
        self.val = self.getVal()
        self.first = True
        self.score = 0
        self.timer = 0

        win32gui.MoveWindow(windowHandle, self.relativePosX, self.relativePosY,
                            self.actualHeight, self.actualWidth
                            , True)
        # 5 is for the arrow keys, 0 nop, 1 up, 2 down, 3 left, 4 right
        # 3 is for the mouse, 0 nop, 1 lclick, 2 rclick
        # 2 is for the spacebar, 0 nop, 1 pressed
        # 360 is for the angle of the mouse
        self.action_space = spaces.MultiDiscrete([5, 3, 2, self.actualWidth + 1, self.actualHeight + 1])

        self.observation_space = spaces.Box(low=0, high=255, shape=(self.screenWidth // self.resolutionDivider,
                                                                    self.screenHeight // self.resolutionDivider),
                                            dtype=np.uint8)

    def moveRelativeToWindow(self, mouseX, mouseY):
        mouseX += self.relativePosX + 8
        mouseY += self.relativePosY
        setMousePos(mouseX, mouseY)

    def clickRelativeToWindow(self, mouseX, mouseY):
        mouseX += self.relativePosX + 8
        mouseY += self.relativePosY
        # print(mouseX, mouseY)
        win32api.SetCursorPos((mouseX, mouseY))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, mouseX, mouseY, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, mouseX, mouseY, 0, 0)

    def isDead(self):
        val = self.getVal()
        # img = screenshot(self.relativePosX + 8 + 112, self.relativePosY + 503, 1, 1, gray=False)
        # print(img[0][0])
        # print(val)
        if val != 18:
            return True
        else:
            return False

    def getVal(self):
        offsets = [0xC, 0x0, 0x10]
        isDead = self.process.get_pointer(0x01EE9890, offsets=offsets)
        val = self.process.read(isDead)
        return val

    def getScore(self):
        offsets = [0xD90]
        score = self.process.get_pointer(0x01EE9890, offsets=offsets)
        val = self.process.read(score)
        return val

    def reset(self):
        self.timer = 0
        self.clickRelativeToWindow(100, 50)
        print("Resetting")
        dead = self.isDead()
        if self.first:
            mainMenuToAct1()
            suicide()
            self.first = False
        else:
            if not dead:
                press('esc')
                time.sleep(0.5)
                press('w')
                press('enter')
                time.sleep(3)
                mainMenuToAct1()
                suicide()
            else:
                press('r')
                time.sleep(0.1)
                press('r')
                time.sleep(0.1)
                press('r')

        self.clickRelativeToWindow(self.windowCenterX, self.windowCenterY)

        return screenshot(self.relativePosX + 8, self.relativePosY, self.actualHeight,
                          self.actualWidth)

    def step(self, action):

        # print("Action")
        if keyboard.is_pressed('q'):
            exit()

        image = screenshot(self.relativePosX + 8, self.relativePosY, self.actualHeight,
                           self.actualWidth)

        score = self.getScore()

        reward = -0.01

        if score != self.score:
            reward = (score - self.score) // 1000
            self.score = score
            self.timer = 0
        else:
            self.timer += 1

        done = self.isDead()

        if self.timer >= 30:
            done = True

        # print(action)
        x, y = win32api.GetCursorPos()

        if action[3] == self.actualWidth + 1:
            moveX = x
        else:
            moveX = action[3]
        if action[4] == self.actualHeight + 1:
            moveY = y
        else:
            moveY = action[4]

        self.moveRelativeToWindow(moveX, moveY)

        if action[0] == 1:
            press('w')
        elif action[0] == 2:
            press('s')
        elif action[0] == 3:
            press('a')
        elif action[0] == 4:
            press('d')

        if action[1] == 1:
            x, y = win32api.GetCursorPos()
            click(x, y)
        elif action[1] == 2:
            x, y = win32api.GetCursorPos()
            rightClick(x, y)

        if action[2] == 1:
            press('spacebar')

        info = {}

        return image, reward, done, info

    def render(self, mode='console'):
        pass

    def close(self):
        pass

# env = hotlinemiami_env()

# env.reset()

# pyautogui.moveTo(-1437, 265 , 1)

# while True:
# x, y = win32api.GetCursorPos()
# print(x, y)
# env.step(env.action_space.sample())
# print(env.action_space.sample())
# print(np.array([1, 2, 3]))
# env.step(env.action_space.sample())

# while True:
# x, y = win32api.GetCursorPos()
# print(x, y)
