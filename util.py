import sys
import time

from python_imagesearch.imagesearch import imagesearch

if sys.platform.startswith("win"):
    import pydirectinput as pdx
else:
    import pyautogui as pdx


def find_image(image, precision=0.8):
    s = imagesearch(image, precision)
    if s[0] == -1 or s[1] == -1:
        return None
    return s


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
