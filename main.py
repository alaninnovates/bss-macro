#  Stumpy Macro - Easy to use macro for Bee Swarm Simulator
#  Copyright (C) 2023. Alan Chen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import multiprocessing
import os
import signal
import sys
import typing
import webbrowser
import time

import mss
import pyautogui
import pywinauto
from python_imagesearch.imagesearch import imagesearch

import gui
import paths
import patterns
import settings
import webhook
from util import key_press, find_image, rotate_camera, zoom_out, import_pdx

import psutil
from pynput import keyboard

pdx = import_pdx()


def exit_macro():
    os.kill(os.getpid(), signal.SIGTERM)


class DisconnectManager:
    def __init__(self):
        self.connected = False
        self.is_reconnecting = False
        self.reconnect_attempts = 0

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
        self.reconnect_attempts += 1
        if self.reconnect_attempts == 1:
            webbrowser.open(settings.get_setting('vip_url'))
        elif self.reconnect_attempts >= 2:
            webbrowser.open('https://www.roblox.com/games/1537690962/Bee-Swarm-Simulator')
            time.sleep(10)
            x, y = imagesearch('assets/playbutton.png')
            print(f'Clicked Play ({x}, {y})')
            pyautogui.click(x, y)

    def activate_roblox(self):
        pid = self.get_roblox_pid()
        if sys.platform.startswith("win"):
            w = pywinauto.Application().connect(process=pid).top_window()
            w.minimize()
            w.maximize()
            w.set_focus()
        elif sys.platform.startswith('darwin'):
            os.system("osascript -e 'activate application \"Roblox\"'")
            time.sleep(0.5)

    def disconnect_check(self):
        if self.is_reconnecting:
            return
        if self.is_connected():
            self.connected = True
        print(find_image('assets/disconnected.png'), self.is_connected())
        if find_image('assets/disconnected.png') or not self.is_connected():
            send_status_message('Disconnected', 0xff0000)
            self.is_reconnecting = True
            loc = find_image('assets/reconnect.png')
            if loc:
                x, y = loc[0], loc[1]
                pyautogui.click(x, y)
                print(f'Clicked Reconnect ({x}, {y})')
                send_status_message("Reconnecting", 0xffff00)
            else:
                if self.close_roblox():
                    print('Closed roblox')
                    send_status_message("Closed Roblox", 0xffff00)
                else:
                    print('Could not find roblox')
                self.open_roblox()
            print('Opened roblox')
            send_status_message("Opened Roblox", 0xffff00)
            while not self.get_roblox_pid():
                time.sleep(0.5)
            self.activate_roblox()
            total_time_waited = 0
            while not self.is_connected():
                time.sleep(0.5)
                total_time_waited += 0.5
                if total_time_waited > 60:
                    send_status_message("Reconnect Failed\nTook over 60 seconds", 0xff0000)
                    self.is_reconnecting = False
                    self.reconnect_attempts = 0
                    self.disconnect_check()
                    return
            claim_hive_slot()
            self.is_reconnecting = False
            self.connected = True
            send_status_message("Connected", 0x00ff00)


disconnect_manager = DisconnectManager()


class TimeManager:
    def __init__(self):
        self.macro_start_time = time.time()
        self.has_done_mondo = True
        self.has_done_clock = False

    def start(self):
        self.macro_start_time = time.time()
        while True:
            if datetime.time.minute == 0:
                self.has_done_mondo = False
            # 65 mins so we have some extra time
            if time.time() - self.macro_start_time > 65 * 60:
                self.has_done_clock = False
                self.macro_start_time = time.time()
            time.sleep(1)

    def needs_do_mondo(self):
        return not self.has_done_mondo

    def did_mondo(self):
        self.has_done_mondo = True

    def needs_do_clock(self):
        return not self.has_done_clock

    def did_clock(self):
        self.has_done_clock = True


time_manager = TimeManager()


def send_status_message(message, color):
    webhook.send_embed(settings.get_setting('webhook_url'),
                       description=f'[{datetime.datetime.now().strftime("%H:%M:%S")}] {message}', color=color)


def is_e_on_screen():
    s = imagesearch('assets/e2.png')
    return not (s[0] == -1 or s[1] == -1)


def claim_hive_slot():
    key_press("w", 2.1)
    key_press("d", 4)
    while not is_e_on_screen():
        key_press("a", 0.3)
    key_press("e")


# todo: does not work at night
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


def do_mondo():
    time.sleep(1.2)
    key_press("space")
    key_press("space")
    pdx.keyDown("s")
    time.sleep(0.8)
    pdx.keyUp("s")
    key_press("space")
    time.sleep(1.5)
    key_press("a", 1.8)
    key_press("d", 2.4)
    key_press("a", 0.6)
    # 2 mins
    time.sleep(2 * 60)


def do_clock():
    time.sleep(1)
    key_press("space")
    key_press("space")
    pdx.keyDown("a")
    pdx.keyDown("w")
    time.sleep(5)
    pdx.keyUp("w")
    time.sleep(1)
    pdx.keyUp("a")
    key_press("d", 1.5)
    key_press("a", 1.5)
    key_press("e")


screen = mss.mss()


def field_drift_compensation():
    # todo: actually make field drift compensation
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


def get_backpack_percent():
    w, h = 1920, 1080
    x = w // 2 + 59 + 3
    y = 6
    bp_color = pyautogui.pixel(x, y)
    backpack_percent = 0
    if bp_color == (105, 0, 0) or not bp_color:  # lte 50%
        return
    if bp_color == (153, 204, 0):  # lte 75%
        if bp_color == (133, 0, 0):  # lte 65%
            if bp_color == (123, 0, 0):  # lte 60%
                # todo stuff
                pass
            elif bp_color == (0, 0, 0):  # gt 60%
                # todo stuff
                pass
        else:  # gt 65%
            # todo stuff
            pass
    else:  # gt 75%
        if bp_color == (196, 0, 0):  # lte 90%
            # todo stuff
            pass
        else:  # gt 90%
            # todo stuff
            pass
    return backpack_percent


def convert_if_possible():
    if not is_e_on_screen():
        return
    key_press("e")
    time.sleep(1)
    while is_e_on_screen():
        time.sleep(1)


def macro_sequence():
    print("Starting macro sequence")
    send_status_message("Starting macro sequence", 0x00ff00)
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
        if settings.get_setting("collect/mondo_buff") and time_manager.needs_do_mondo():
            do_mondo()
            time_manager.did_mondo()
            continue
        if settings.get_setting("collect/clock") and time_manager.needs_do_clock():
            do_clock()
            time_manager.did_clock()
            continue
        field = settings.get_setting('field')
        send_status_message(f"Going to field: {field}", 0x808080)
        paths.go_to_field(field)
        time.sleep(1)
        # place sprinkler
        key_press("1")
        gather_time = settings.get_setting('gather_time')
        send_status_message(f"Gathering: {field}\nTime limit: {gather_time} minutes", 0x22a338)
        start_farm_time = time.time()
        gather_time_limit = gather_time * 60
        pattern_name = settings.get_setting('pattern')
        fill_percent = settings.get_setting('fill_percent')
        while True:
            patterns.farm_pattern(pattern_name)
            # field_drift_compensation()
            if get_backpack_percent() >= fill_percent:
                send_status_message(f"Gathering: Ended\nReason: Backpack limit ({fill_percent}%)", 0x22a338)
                break
            # print(time.time(), time.time() - start_farm_time)
            if time.time() - start_farm_time >= gather_time_limit:
                send_status_message("Gathering: Ended\nReason: Time limit", 0x22a338)
                break
        pdx.mouseUp()
        send_status_message("Returning to hive", 0x808080)


def disconnect_loop():
    while True:
        print("Checking")
        disconnect_manager.disconnect_check()
        time.sleep(1)


def run_macro():
    seq_proc = multiprocessing.Process(target=macro_sequence)
    seq_proc.start()
    dc_proc = multiprocessing.Process(target=disconnect_loop)
    dc_proc.start()
    time.sleep(1)
    while True:
        if not disconnect_manager.is_connected():
            print("Killling seq_proc")
            seq_proc.kill()
            while not disconnect_manager.is_connected():
                print("Waiting for reconnect", disconnect_manager.is_connected())
                time.sleep(1)
            seq_proc.terminate()
            print("Restarting seq_proc")
            seq_proc = multiprocessing.Process(target=macro_sequence)
            seq_proc.start()
        time.sleep(0.1)


def watch_for_hotkeys():
    is_running = False
    run_proc: typing.Optional[multiprocessing.Process] = None

    def on_press(key):
        nonlocal run_proc, is_running
        if key == keyboard.Key.f3:
            print("Exiting")
            send_status_message("Exiting macro", 0xffffff)
            if run_proc:
                run_proc.kill()
            exit_macro()
        elif key == keyboard.Key.f1:
            if is_running:
                print("Macro already running")
                return
            print("Running macro")
            send_status_message("Running macro", 0xa8329e)
            run_proc = multiprocessing.Process(target=run_macro)
            run_proc.start()
            is_running = True

    keyboard.Listener(on_press=on_press).start()


if __name__ == "__main__":
    try:
        print("Starting macro")
        send_status_message("Starting macro gui", 0x808080)
        watch_for_hotkeys()
        gui.gui()
        # field_drift_compensation()
    except KeyboardInterrupt:
        print("Macro stopped")
        exit_macro()
