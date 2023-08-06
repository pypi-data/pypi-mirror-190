try: from pyautogui import typewrite
except: from os import system; system('start python -m pip install pyautogui'); from pyautogui import typewrite
from time import sleep
from random import randfloat

def realistictype(text):
	letters = text.split()
	for letter in letters:
		typewrite(letter)
		sleep(randfloat(0.1, 1.0))


