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


class yfinance_env(gym.Env):

    def __init__(self):
        pass

    def reset(self):
        pass

    def step(self, action):
        pass
        return image, reward, done, info

    def render(self, mode='console'):
        pass

    def close(self):
        pass
