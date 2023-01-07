import json
import os


default_settings = {
        "webhook_url": "",
        "vip_url": "https://www.roblox.com/games/4189852503?privateServerLinkCode=94175309348158422142147035472390",
        "gather_time": 9,
    }


def read_settings():
    if not os.path.exists("macro-settings.json"):
        return default_settings
    with open("macro-settings.json") as f:
        data = json.load(f)
        return data


def get_setting(setting):
    return read_settings()[setting]


def set_setting(setting, value):
    settings = read_settings()
    settings[setting] = value
    json.dump(settings, open("macro-settings.json", "w"))
