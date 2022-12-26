import os
import signal
import sys
import threading
import webbrowser
import time

import pyautogui
from python_imagesearch.imagesearch import imagesearch

if sys.platform.startswith("win"):
    import pydirectinput as pdx
    import pywinauto
else:
    import pyautogui as pdx

import psutil
from pynput import keyboard


def exit_macro():
    os.kill(os.getpid(), signal.SIGTERM)


pixelRatio = pyautogui.screenshot().size[0] / pyautogui.size().width


# todo: maybe use imagesearch
def locate_center(image):
    loc = pyautogui.locateCenterOnScreen(image)
    if loc:
        x, y = loc[0] / pixelRatio, loc[1] / pixelRatio
        return x, y
    else:
        return None


def find_image(image):
    s = imagesearch(image)
    if s[0] == -1 or s[1] == -1:
        return None
    return s


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
    time.sleep(10)
    x, y = imagesearch('assets/playbutton.png')
    pyautogui.click(x, y)


def activate_roblox():
    pid = get_roblox_pid()
    if sys.platform.startswith("win"):
        w = pywinauto.Application().connect(process=pid).top_window()
        w.minimize()
        w.maximize()
        w.set_focus()
    # todo: mac


connected = False
is_reconnecting = False


def disconnect_check():
    global connected, is_reconnecting
    if is_reconnecting:
        return
    if get_roblox_pid():
        connected = True
    if find_image('assets/disconnected.png') or get_roblox_pid() is None:
        print('Disconnected')
        is_reconnecting = True
        loc = find_image('assets/reconnect.png')
        if loc:
            x, y = loc[0], loc[1]
            pyautogui.click(x, y)
            print(f'Clicked Reconnect ({x}, {y})')
        else:
            if close_roblox():
                print('Closed roblox')
            else:
                print('Could not find roblox')
            open_roblox()
        print('Opened roblox')
        while not get_roblox_pid():
            time.sleep(0.1)
        # wait for game to load
        time.sleep(60)
        activate_roblox()
        claim_hive_slot()
        is_reconnecting = False
        connected = True


def key_press(key, duration=0):
    pdx.keyDown(key)
    time.sleep(duration)
    pdx.keyUp(key)


def is_e_on_screen():
    s = imagesearch('assets/e.png')
    return not (s[0] == -1 or s[1] == -1)


def claim_hive_slot():
    key_press("w", 2.1)
    key_press("d", 4)
    while not is_e_on_screen():
        key_press("a", 0.3)
    key_press("e")


def rotate_camera(times=1):
    camera_rotation_loops = abs(times) % 8
    for _ in range(camera_rotation_loops):
        key_press(times > 0 and "," or ".")


def zoom_out(times=1):
    for _ in range(times):
        key_press("o")


def zoom_in(times=1):
    for _ in range(times):
        key_press("i")


# there are many cases here - some do not work
# todo: fix everything!
def face_hive(enable):
    for _ in range(4):
        for _ in range(2):
            if find_image("assets/hivecomb.png"):
                if enable:
                    rotate_camera(4)
                return
            zoom_out()
            found_g = find_image("assets/hivegift.png")
            zoom_in()
            if found_g:
                if enable:
                    rotate_camera(4)
                return
            rotate_camera(4)
            time.sleep(1)
        reset()
    # client frozen


def go_to_cannon():
    key_press("w", 1)
    key_press("d", 10)
    key_press("space")
    key_press("d", 1.2)


def reset():
    key_press("escape")
    time.sleep(0.1)
    key_press("r")
    time.sleep(0.1)
    key_press("enter")


def go_to_pine_tree():
    time.sleep(0.8)
    key_press("space")
    key_press("space")
    pdx.keyDown("sd")
    pdx.keyDown("s")
    time.sleep(3)
    pdx.keyUp("s")
    time.sleep(1.6)
    pdx.keyUp("d")
    key_press("space")


def farm_e_lol():
    for i in range(2):
        key_press("w", 1)
        key_press("a", 0.1)
        key_press("s", 1)
        key_press("a", 0.1)
    for i in range(2):
        key_press("w", 1)
        key_press("d", 0.1)
        key_press("s", 1)
        key_press("d", 0.1)


def main_loop():
    global connected
    threading.Thread(target=disconnect_loop).start()
    while not connected:
        time.sleep(0.1)
    time.sleep(1)
    reset()
    time.sleep(8)
    face_hive(True)
    time.sleep(8)
    zoom_out(5)
    time.sleep(1)
    go_to_cannon()
    key_press("e")
    go_to_pine_tree()
    time.sleep(1)
    # place sprinkler
    key_press("1")
    rotate_camera(6)
    start_farm_time = time.time()
    while True:
        farm_e_lol()
        # 30 seconds
        if time.time() - start_farm_time == 30:
            break
    print('Wow')


def disconnect_loop():
    while True:
        print("Checking")
        disconnect_check()
        time.sleep(1)


def watch_for_quit():
    def on_press(key):
        if key != keyboard.Key.f3:
            return
        print("Exiting")
        exit_macro()

    keyboard.Listener(on_press=on_press).start()


if __name__ == "__main__":
    try:
        print("Starting macro.")
        watch_for_quit()
        main_loop()
    except KeyboardInterrupt:
        print("Macro stopped.")
        exit_macro()
