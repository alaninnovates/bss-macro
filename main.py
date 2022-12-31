import multiprocessing
import os
import signal
import sys
import webbrowser
import time

import tkinter as tk

import pyautogui
from python_imagesearch.imagesearch import imagesearch

import webhook

if sys.platform.startswith("win"):
    import pydirectinput as pdx
    import pywinauto
else:
    import pyautogui as pdx

import psutil
from pynput import keyboard


webhook_client = webhook.WebhookClient(url="https://discord.com/api/webhooks/1058279840400289833"
                                           "/rA_QhX9_TxIY3cBqbRNydTlr8ijyXMpPhjZKK5uQBu0AbbmCFrTMY2RjQIzUGjWzw7Ll")


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


def find_image(image, precision=0.8):
    s = imagesearch(image, precision)
    if s[0] == -1 or s[1] == -1:
        return None
    return s


class DisconnectManager:
    def __init__(self):
        self.connected = False
        self.is_reconnecting = False

    def get_roblox_pid(self):
        running_apps = psutil.process_iter(['pid', 'name'])
        for app in running_apps:
            try:
                if app.name().lower().startswith('roblox'):
                    return app.pid
            except psutil.Error:
                pass
        return None

    def is_connected(self):
        return bool(find_image('assets/sprinkler.png')) and bool(self.get_roblox_pid())

    def close_roblox(self):
        pid = self.get_roblox_pid()
        if not pid:
            return False
        os.kill(pid, 9)
        return True

    def open_roblox(self):
        webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
        time.sleep(10)
        x, y = imagesearch('assets/playbutton.png')
        pyautogui.click(x, y)

    def activate_roblox(self):
        pid = self.get_roblox_pid()
        if sys.platform.startswith("win"):
            w = pywinauto.Application().connect(process=pid).top_window()
            w.minimize()
            w.maximize()
            w.set_focus()
        # todo: mac

    def disconnect_check(self):
        if self.is_reconnecting:
            return
        if self.is_connected():
            self.connected = True
        print(find_image('assets/disconnected.png'), self.is_connected())
        if find_image('assets/disconnected.png') or not self.is_connected():
            print('Disconnected')
            self.is_reconnecting = True
            loc = find_image('assets/reconnect.png')
            if loc:
                x, y = loc[0], loc[1]
                pyautogui.click(x, y)
                print(f'Clicked Reconnect ({x}, {y})')
            else:
                if self.close_roblox():
                    print('Closed roblox')
                else:
                    print('Could not find roblox')
                self.open_roblox()
            print('Opened roblox')
            while not self.is_connected():
                time.sleep(0.5)
            # wait for game to load
            time.sleep(60)
            self.activate_roblox()
            claim_hive_slot()
            self.is_reconnecting = False
            self.connected = True


disconnect_manager = DisconnectManager()


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


def face_hive(enable):
    for _ in range(2):
        for _ in range(4):
            print(find_image("assets/hivecomb.png"))
            if find_image("assets/hivecomb.png"):
                if enable:
                    rotate_camera(4)
                return
            rotate_camera(4)
            time.sleep(1)
        reset()
        time.sleep(8)
    # client frozen probs
    print("Face_hive done")


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


# todo: lag affects this a TON. it can land in different places every time
def go_to_pine_tree():
    webhook_client.send_embed(description="Going to field: Pine Tree", color=0xff0000)
    time.sleep(0.8)
    key_press("space")
    key_press("space")
    pdx.keyDown("d")
    pdx.keyDown("s")
    time.sleep(3)
    pdx.keyUp("s")
    time.sleep(1.8)
    pdx.keyUp("d")
    key_press("space")


def farm_e_lol():
    pdx.mouseDown()
    for i in range(2):
        key_press("w", 0.72)
        key_press("a", 0.1)
        key_press("s", 0.72)
        key_press("a", 0.1)
    for i in range(2):
        key_press("w", 0.72)
        key_press("d", 0.1)
        key_press("s", 0.72)
        key_press("d", 0.1)


def field_drift_compensation():
    pass


def macro_sequence():
    while True:
        reset()
        time.sleep(8)
        face_hive(True)
        print("Face_hive continue in main")
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
        webhook_client.send_embed(description="Gathering", color=0xff0000)
        start_farm_time = time.time()
        while True:
            farm_e_lol()
            field_drift_compensation()
            # 30 seconds
            print(time.time(), time.time() - start_farm_time)
            if time.time() - start_farm_time >= 30:
                break
        pdx.mouseUp()
        webhook_client.send_embed(description="Returning to hive", color=0xff0000)


def disconnect_loop():
    while True:
        print("Checking")
        disconnect_manager.disconnect_check()
        time.sleep(1)


def run_macro():
    # todo: make the seq_proc restart after a disconnect
    seq_proc = multiprocessing.Process(target=macro_sequence)
    seq_proc.start()
    dc_proc = multiprocessing.Process(target=disconnect_loop)
    dc_proc.start()
    while True:
        if not disconnect_manager.connected:
            seq_proc.kill()
        time.sleep(0.1)


def watch_for_hotkeys():
    def on_press(key):
        if key == keyboard.Key.f3:
            print("Exiting")
            webhook_client.send_embed(description="Exiting macro", color=0xff0000)
            exit_macro()
        elif key == keyboard.Key.f1:
            print("Running macro")
            webhook_client.send_embed(description="Running macro", color=0xff0000)
            run_macro()

    keyboard.Listener(on_press=on_press).start()


def gui():
    root = tk.Tk()
    tk.Label(root, text="Hello").pack()
    root.mainloop()


if __name__ == "__main__":
    try:
        print("Starting macro")
        webhook_client.send_embed(description="Starting macro gui", color=0xff0000)
        watch_for_hotkeys()
        gui()
    except KeyboardInterrupt:
        print("Macro stopped")
        exit_macro()
