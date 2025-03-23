import time
import os
import pyautogui
import cv2
import pytesseract
import webbrowser
import numpy as np
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def reactionTime():
    webbrowser.open("https://humanbenchmark.com/tests/reactiontime")
    time.sleep(3)
    print("Starting Reaction Time test...")
    pyautogui.click(960,540)
    for attempt in range(5):
        print(f"Attempt {attempt + 1}/5: Waiting for the screen to turn green...")
        while True:
            screen = ImageGrab.grab()
            pixel = screen.getpixel((960, 540))  # adjust coordinates if needed
            # outputs rgb values of that coordinate
            if pixel[1] > 200 and pixel[0] < 100:  # green detection
                pyautogui.click()
                print("Clicked!")
                break
            
            time.sleep(0.01)
        time.sleep(2)
        pyautogui.click()
        time.sleep(1)
    
    print("Test completed.")
    pyautogui.hotkey("alt","tab")


def aimTrainer():
    target = cv2.imread("target.png",cv2.IMREAD_GRAYSCALE)
    if target is None:
        raise ValueError("Error loading target.png! Make sure the file exists in the script's directory.")
    webbrowser.open("https://humanbenchmark.com/tests/aim")
    time.sleep(3)
    print("Starting Aim Trainer test...")

    while True:
        screen = np.array(ImageGrab.grab())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)  # convert to grayscale
        # template matching
        result = cv2.matchTemplate(screen_gray, target, cv2.TM_CCOEFF_NORMED)
        threshold = 0.93  # Adjust this if needed (0.8-0.99)
        locations = np.where(result >= threshold)
        for pt in zip(*locations[::-1]):
            target_x = pt[0] + target.shape[1] // 2
            target_y = pt[1] + target.shape[0] // 2
            pyautogui.click(target_x, target_y)
            print(f"Clicked target at ({target_x}, {target_y})")
            time.sleep(0.03)  # Small delay to avoid double-clicking
# unfinished, work on way to break loop


def numberMemory():
    score = int(input("Input the score you want to get: "))
    input("Make sure your browser is in fullscreen and press Enter:")
    webbrowser.open("https://humanbenchmark.com/tests/number-memory")
    time.sleep(3)
    print("Starting the test...")
    pyautogui.click(960, 585)
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789' # filter for numbers
    for levels in range(score):
        print(f"Level {levels + 1}")
        screen = ImageGrab.grab(bbox=(464,212,1156,485))
        text = pytesseract.image_to_string(screen, config=config)
        time.sleep(3)
        print(screen)
        print(text)
        pyautogui.click(950,440)
        pyautogui.write(text)
        pyautogui.press("enter")
        time.sleep(1)

    print("Test completed.")
    pyautogui.hotkey("alt","tab")


def typing():
    wpm = int(input("Input words per minute (wpm):"))
    input("Make sure your browser is in fullscreen and press Enter:")
    webbrowser.open("https://humanbenchmark.com/tests/typing")
    time.sleep(3)
    screen = ImageGrab.grab(bbox=(470,370,1440,610))
    text = pytesseract.image_to_string(screen).replace("\n"," ").strip()
    print("Text Found! Typing...")
    charList = list(text)
    pyautogui.click(950,540)
    time.sleep(1)
    delay = 60/(wpm*5)
    pyautogui.write(charList,delay)
    print("Done!")
    pyautogui.hotkey("alt","tab")


def verbalMemory():
    score = int(input("Enter the score you want to get:"))
    webbrowser.open("https://humanbenchmark.com/tests/verbal-memory")
    time.sleep(3)
    pyautogui.click(950,600)
    wordList = []
    for level in range(score):
        print(f"Level {level + 1}")
        screen = ImageGrab.grab(bbox=(730,385,1150,480))
        text = pytesseract.image_to_string(screen)
        if not (text in wordList):
            wordList.append(text)
            print("NEW")
            pyautogui.click(1020,520)
        else:
            print("SEEN")
            pyautogui.click(885,515)
    print("Done!")
    pyautogui.hotkey("alt","tab")


def main():
    print(" ______                    __                         __         ______         __   ")
    print("|   __ \\.-----.-----.----.|  |--.--------.---.-.----.|  |--.    |   __ \\.-----.|  |_ ")
    print("|   __ <|  -__|     |  __||     |        |  _  |   _||    <     |   __ <|  _  ||   _|")
    print("|______/|_____|__|__|____||__|__|__|__|__|___._|__|  |__|__|    |______/|_____||____|")
    while True:
        print("\n1. Reaction Time Test")
        print("2. Aim Trainer")
        print("3. Number Memory")
        print("4. Typing Test")
        print("5. Verbal Memory")
        print("6. Exit")
        print("\nINSTRUCTIONS: Make sure your browser is in fullscreen when starting the script and there is nothing \nin the way to interfere with the bot. \nMake sure you have the requirements from 'dependencies.txt' installed. \nRecommended to be on 1920x1080 resolution, other resolutions currently untested.\n")
        time.sleep(2)
        choice = input("\nPlease select a choice >> ")
        
        if choice == "1":
            reactionTime()
            os.system("cls")
        elif choice == "2":
            aimTrainer()
            os.system("cls")
        elif choice == "3":
            print("Number Memory is currently unfinished and may have unexpected results.")
            numberMemory()
            os.system("cls")
        elif choice == "4":
            typing()
            os.system("cls")
        elif choice == "5":
            verbalMemory()
            os.system("cls")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

main()
