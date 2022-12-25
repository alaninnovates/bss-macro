import os
import webbrowser
import time

import pyautogui
# import pydirectinput

import psutil

pixelRatio = pyautogui.screenshot().size[0] / pyautogui.size().width


def locate_center(image):
    loc = pyautogui.locateCenterOnScreen(image)
    if loc:
        x, y = loc[0] / pixelRatio, loc[1] / pixelRatio
        return x, y
    else:
        return None


def close_roblox():
    running_apps = psutil.process_iter(['pid', 'name'])
    closed = False
    for app in running_apps:
        try:
            if app.name().lower().startswith('roblox'):
                os.kill(app.pid, 9)
                print('Killed roblox', app.pid)
                closed = True
            else:
                pass
        except psutil.Error:
            pass
    return closed


def open_roblox():
    webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
    time.sleep(5)
    x, y = locate_center('assets/playbutton.png')
    pyautogui.click(x, y)


def disconnect_check():
    if pyautogui.locateCenterOnScreen('assets/disconnected.png'):
        print('Disconnected')
        loc = locate_center('assets/reconnect.png')
        if loc:
            x, y = loc[0] / pixelRatio, loc[1] / pixelRatio
            pyautogui.click(x, y)
            print(f'Clicked Reconnect ({x}, {y})')
        else:
            if close_roblox():
                print('Closed roblox')
            else:
                print('Could not find roblox')
            open_roblox()


# while True:
#     disconnect_check()
#     time.sleep(1)

open_roblox()