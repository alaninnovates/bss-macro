import multiprocessing
import os
import re
import signal
import sys
import typing
import webbrowser
import time

import tkinter as tk

import mss
import pyautogui
from python_imagesearch.imagesearch import imagesearch

import settings
import webhook

if sys.platform.startswith("win"):
    import pydirectinput as pdx
    import pywinauto
else:
    import pyautogui as pdx

import psutil
from pynput import keyboard


def exit_macro():
    os.kill(os.getpid(), signal.SIGTERM)


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
        return bool(find_image('assets/sprinkler2.png')) and bool(self.get_roblox_pid())

    def close_roblox(self):
        pid = self.get_roblox_pid()
        if not pid:
            return False
        os.kill(pid, 9)
        return True

    def open_roblox(self):
        # webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
        # time.sleep(10)
        # x, y = imagesearch('assets/playbutton.png')
        # pyautogui.click(x, y)
        # webbrowser.open(
        #     'https://www.roblox.com/games/1537690962/x2-Event-Bee-Swarm-Simulator?privateServerLinkCode=54294896913853942846549719787777')
        webbrowser.open(settings.get_setting('vip_url'))

    def activate_roblox(self):
        pid = self.get_roblox_pid()
        if sys.platform.startswith("win"):
            w = pywinauto.Application().connect(process=pid).top_window()
            w.minimize()
            w.maximize()
            w.set_focus()
        elif sys.platform.startswith('darwin'):
            os.system("oascript -e 'activate application \"Roblox\"'")
            time.sleep(0.5)

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
            while not self.get_roblox_pid():
                time.sleep(0.5)
            self.activate_roblox()
            while not self.is_connected():
                time.sleep(0.5)
            claim_hive_slot()
            self.is_reconnecting = False
            self.connected = True


disconnect_manager = DisconnectManager()


def key_press(key, duration: float = 0):
    pdx.keyDown(key)
    time.sleep(duration)
    pdx.keyUp(key)


def is_e_on_screen():
    s = imagesearch('assets/e2.png')
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
                print("Face_hive done")
                return
            rotate_camera(4)
            time.sleep(1)
        reset()
        time.sleep(8)
    # client frozen probs


def go_to_cannon():
    key_press("w", 1)
    key_press("d", 10)
    key_press("space")
    pdx.keyDown("d")
    while not is_e_on_screen():
        time.sleep(0.1)
    pdx.keyUp("d")


def reset():
    key_press("escape")
    time.sleep(0.1)
    key_press("r")
    time.sleep(0.1)
    key_press("enter")


def go_to_pine_tree():
    time.sleep(0.4)
    key_press("space")
    key_press("space")
    pdx.keyDown("d")
    pdx.keyDown("s")
    time.sleep(3)
    pdx.keyUp("s")
    time.sleep(1.7)
    pdx.keyUp("d")
    key_press("space")
    rotate_camera(6)


def go_to_stump():
    time.sleep(1.7)
    key_press("space")
    key_press("space")
    pdx.keyDown("a")
    time.sleep(4)
    pdx.keyUp("a")
    rotate_camera(2)
    key_press("w", 0.8)


def go_to_pineapple():
    time.sleep(1.7)
    key_press("space")
    key_press("space")
    pdx.keyDown("a")
    time.sleep(2.5)
    pdx.keyUp("a")
    key_press("space")
    rotate_camera(4)
    key_press("w", 1)


def go_to_field(field):
    webhook.send_embed(settings.get_setting('webhook_url'), description=f"Going to field: {field}", color=0xff0000)
    if field == "Pine Tree":
        go_to_pine_tree()
    elif field == "Stump":
        go_to_stump()
    elif field == "Pineapple":
        go_to_pineapple()


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


screen = mss.mss()


def field_drift_compensation():
    # this func doesn't work atm
    pass
    # goal: make saturator in center of screen
    # use wasd keys to position camera
    for _ in range(5):
        saturator_pos = find_image("assets/saturator.png", 0.5)
        if not saturator_pos:
            break
        saturator_x, saturator_y = saturator_pos[0], saturator_pos[1]
        # window_width, window_height = screen.monitors[0]["width"], screen.monitors[0]["height"]
        window_width, window_height = 1920, 1080
        print(saturator_x, saturator_y, window_width, window_height)
        win_up = window_height / 2.14
        win_down = window_height / 1.88
        win_left = window_width / 2.14
        win_right = window_width / 1.88
        if win_left <= saturator_x <= win_right and win_up <= saturator_y <= win_down:
            print("Saturator in center")
            break
        if saturator_x < win_left:
            pdx.keyDown("a")
        elif saturator_x > win_right:
            pdx.keyDown("d")
        if saturator_y < win_up:
            pdx.keyDown("w")
        elif saturator_y > win_down:
            pdx.keyDown("s")
        time.sleep(0.2)
        pdx.keyUp("a")
        pdx.keyUp("d")
        pdx.keyUp("w")
        pdx.keyUp("s")


def convert_if_possible():
    if not is_e_on_screen():
        return
    key_press("e")
    time.sleep(1)
    while is_e_on_screen():
        time.sleep(1)


def macro_sequence():
    print("Starting macro sequence")
    while True:
        reset()
        time.sleep(8)
        face_hive(True)
        print("Face_hive continue in main")
        zoom_out(5)
        convert_if_possible()
        time.sleep(1)
        go_to_cannon()
        key_press("e")
        go_to_field(settings.get_setting('field'))
        time.sleep(1)
        # place sprinkler
        key_press("1")
        webhook.send_embed(settings.get_setting('webhook_url'), description="Gathering", color=0xff0000)
        start_farm_time = time.time()
        gather_time_limit = settings.get_setting('gather_time') * 60
        while True:
            farm_e_lol()
            # field_drift_compensation()
            print(time.time(), time.time() - start_farm_time)
            if time.time() - start_farm_time >= gather_time_limit:
                break
        pdx.mouseUp()
        webhook.send_embed(settings.get_setting('webhook_url'), description="Returning to hive", color=0xff0000)


def disconnect_loop():
    while True:
        print("Checking")
        disconnect_manager.disconnect_check()
        time.sleep(1)


def run_macro():
    # todo: make the seq_proc restart after a disconnect
    seq_proc = multiprocessing.Process(target=macro_sequence)
    seq_proc.run()
    dc_proc = multiprocessing.Process(target=disconnect_loop)
    dc_proc.run()
    while True:
        if not disconnect_manager.connected:
            seq_proc.kill()
        time.sleep(0.1)


def watch_for_hotkeys():
    is_running = False
    run_proc: typing.Optional[multiprocessing.Process] = None

    def on_press(key):
        nonlocal run_proc, is_running
        print(key)
        if key == keyboard.Key.f3:
            print("Exiting")
            webhook.send_embed(settings.get_setting('webhook_url'), description="Exiting macro", color=0xff0000)
            if run_proc:
                run_proc.kill()
            exit_macro()
        elif key == keyboard.Key.f1:
            if is_running:
                print("Macro already running")
                return
            print("Running macro")
            webhook.send_embed(settings.get_setting('webhook_url'), description="Running macro", color=0xff0000)
            run_proc = multiprocessing.Process(target=run_macro)
            run_proc.start()
            is_running = True

    keyboard.Listener(on_press=on_press).start()


class ValidatedEntry(tk.Entry):
    def __init__(self, master, vcmd, setting_name: str, setting_var: tk.Variable, **kwargs):
        self.vcmd = (master.register(vcmd), '%P')
        self.setting_var = setting_var
        self.setting_var.set(settings.get_setting(setting_name))
        self.setting_var.trace_add("write", lambda *args: settings.set_setting(setting_name, self.setting_var.get()))
        super().__init__(master, textvariable=self.setting_var, validate="key", validatecommand=self.vcmd, **kwargs)


def is_int(p):
    try:
        int(p)
        return True
    except ValueError:
        return False


vip_regex = r"^((http(s)?):\/\/)?((www|web)\.)?roblox\.com\/games\/(1537690962|4189852503)\/?([" \
            r"^\/]*)\?privateServerLinkCode=.{32}(\&[^\/]*)*$"


def validate_vip(p):
    pattern = re.compile(vip_regex)
    return pattern.match(p) is not None


def gui():
    root = tk.Tk()
    vip_url = tk.StringVar()
    webhook_url = tk.StringVar()
    gather_time = tk.IntVar()
    root.geometry("300x300")
    root.title("Stumpy Macro")
    tk.Label(root, text="Vip Server:").pack()
    ValidatedEntry(root, validate_vip, "vip_url", vip_url).pack()
    tk.Label(root, text="Webhook URL:").pack()
    ValidatedEntry(root, lambda p: p == "" or p.startswith("http"), "webhook_url", webhook_url).pack()
    tk.Label(root, text="Gather time (mins):").pack()
    ValidatedEntry(root, lambda p: p != "" and is_int(p), "gather_time", gather_time).pack()
    root.mainloop()


if __name__ == "__main__":
    try:
        print("Starting macro")
        webhook.send_embed(settings.get_setting('webhook_url'), description="Starting macro gui", color=0xff0000)
        watch_for_hotkeys()
        gui()
        # field_drift_compensation()
    except KeyboardInterrupt:
        print("Macro stopped")
        exit_macro()
