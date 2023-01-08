import sys
import time

from util import key_press, rotate_camera

if sys.platform.startswith("win"):
    import pydirectinput as pdx
else:
    import pyautogui as pdx


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
