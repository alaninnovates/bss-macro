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

import time

from util import key_press, rotate_camera, import_pdx

pdx = import_pdx()


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


def go_to_rose():
    time.sleep(0.28)
    key_press("space")
    key_press("space")
    pdx.keyDown("d")
    time.sleep(2.8)
    pdx.keyUp("d")
    key_press("space")
