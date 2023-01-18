#  Stumpy Macro - Easy to use macro for Bee Swarm Simulator
#  Copyright (C) 2023 Alan Chen
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

import sys
import time

import pyautogui
from python_imagesearch.imagesearch import imagesearch

if sys.platform.startswith("win"):
    import pydirectinput as pdx
else:
    import pyautogui as pdx


display_scale = pyautogui.screenshot().width / pyautogui.size().width


def find_image(image, precision=0.8):
    s = imagesearch(image, precision)
    if s[0] == -1 or s[1] == -1:
        return None
    return [s[0] // display_scale, s[1] // display_scale]


def key_press(key, duration: float = 0):
    pdx.keyDown(key)
    time.sleep(duration)
    pdx.keyUp(key)


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


def is_int(p):
    try:
        int(p)
        return True
    except ValueError:
        return False


def import_pdx():
    if sys.platform.startswith("win"):
        return __import__("pydirectinput")
    else:
        return __import__("pyautogui")
