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


def get_roblox_pid():
    running_apps = psutil.process_iter(['pid', 'name'])
    for app in running_apps:
        try:
            if app.name().lower().startswith('roblox'):
                return app.pid
        except psutil.Error:
            pass
    return None


def close_roblox():
    pid = get_roblox_pid()
    if not pid:
        return False
    os.kill(pid, 9)
    return True


def open_roblox():
    webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
    time.sleep(5)
    x, y = locate_center('assets/playbutton.png')
    pyautogui.click(x, y)


reconnecting = False


def disconnect_check():
    global reconnecting
    if reconnecting:
        return
    if pyautogui.locateCenterOnScreen('assets/disconnected.png') or get_roblox_pid() is None:
        print('Disconnected')
        reconnecting = True
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
        print('Opened roblox')
        reconnecting = False


while True:
    disconnect_check()
    time.sleep(1)
