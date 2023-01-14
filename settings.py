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

import json
import os

default_settings = {
    "version": 1,
    "webhook_url": "",
    "vip_url": "https://www.roblox.com/games/4189852503?privateServerLinkCode=94175309348158422142147035472390",
    "move_speed": 28,
    "collect": {
        "clock": True,
        "mondo_buff": True
    },
    "gather_time": 9,
    "field": "Pine Tree",
    "pattern": "e_lol",
    "fill_percent": 95,
    "return_method": "Walk",
}


def read_settings():
    if not os.path.exists("macro-settings.json"):
        return default_settings
    with open("macro-settings.json") as f:
        data = json.load(f)
        if data["version"] != default_settings["version"]:
            new_data = migrate_settings(data)
            json.dump(new_data, open("macro-settings.json", "w"))
            return new_data
        return data


def get_setting(setting):
    settings = read_settings()
    if '/' in setting:
        setting = setting.split('/')
        return settings[setting[0]][setting[1]]
    return settings[setting]


def set_setting(setting, value):
    settings = read_settings()
    if '/' in setting:
        setting = setting.split('/')
        settings[setting[0]][setting[1]] = value
    else:
        settings[setting] = value
    json.dump(settings, open("macro-settings.json", "w"))


def migrate_settings(prev_settings):
    print("Migrating settings...")
    for setting in default_settings:
        if setting not in prev_settings:
            prev_settings[setting] = default_settings[setting]
    prev_settings["version"] = default_settings["version"]
    print(f"Successfully migrated settings to settings version {default_settings['version']}")
    return prev_settings
