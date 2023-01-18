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

import re

import tkinter as tk
from tkinter import ttk

import settings
from util import is_int


class ValidatedEntry(tk.Entry):
    def __init__(self, master, vcmd, setting_name: str, setting_var: tk.Variable, **kwargs):
        self.vcmd = (master.register(vcmd), '%P')
        self.setting_var = setting_var
        self.setting_var.set(settings.get_setting(setting_name))
        self.setting_var.trace_add("write", lambda *args: settings.set_setting(setting_name, self.setting_var.get()))
        super().__init__(master, textvariable=self.setting_var, validate="key", validatecommand=self.vcmd, **kwargs)


class BooleanEntry(tk.Checkbutton):
    def __init__(self, master, setting_name: str, setting_var: tk.BooleanVar, **kwargs):
        self.setting_var = setting_var
        self.setting_var.set(settings.get_setting(setting_name))
        self.setting_var.trace_add("write", lambda *args: settings.set_setting(setting_name, self.setting_var.get()))
        super().__init__(master, variable=self.setting_var, **kwargs)


vip_regex = r"^((http(s)?):\/\/)?((www|web)\.)?roblox\.com\/games\/(1537690962|4189852503)\/?([" \
            r"^\/]*)\?privateServerLinkCode=.{32}(\&[^\/]*)*$"


def validate_vip(p):
    pattern = re.compile(vip_regex)
    return pattern.match(p) is not None


def gather_tab_gui(root):
    gather_time = tk.IntVar()
    tk.Label(root, text="Gather time (mins):").pack()
    ValidatedEntry(root, lambda p: p != "" and is_int(p), "gather_time", gather_time, width=10).pack()

    field = tk.StringVar()
    field.set(settings.get_setting('field'))
    tk.Label(root, text="Field:").pack()
    tk.OptionMenu(root, field, "Pine Tree", "Stump", "Pineapple", "Rose").pack()
    field.trace_add("write", lambda *args: settings.set_setting("field", field.get()))

    fill_percent = tk.StringVar()
    fill_percent.set(f'{settings.get_setting("fill_percent")}%')
    tk.Label(root, text="Fill percent:").pack()
    tk.OptionMenu(root, fill_percent,
                  *map(lambda x: f'{x}%', filter(lambda x: x % 5 == 0, list(range(50, 101))))).pack()
    fill_percent.trace_add("write", lambda *args: settings.set_setting("fill_percent", int(fill_percent.get()[:-1])))

    return_method = tk.StringVar()
    return_method.set(settings.get_setting('return_method'))
    tk.Label(root, text="Return method:").pack()
    tk.OptionMenu(root, return_method, "Walk", "Reset").pack()
    return_method.trace_add("write", lambda *args: settings.set_setting("return_method", return_method.get()))


def collect_tab_gui(root):
    collect_clock = tk.BooleanVar()
    BooleanEntry(root, "collect/clock", collect_clock, text="Clock").pack()

    collect_mondo_buff = tk.BooleanVar()
    BooleanEntry(root, "collect/mondo_buff", collect_mondo_buff, text="Mondo Buff").pack()


def settings_tab_gui(root):
    vip_url = tk.StringVar()
    tk.Label(root, text="Vip Server:").pack()
    ValidatedEntry(root, validate_vip, "vip_url", vip_url, width=30).pack()

    webhook_url = tk.StringVar()
    tk.Label(root, text="Webhook URL:").pack()
    ValidatedEntry(root, lambda p: p == "" or p.startswith("http"), "webhook_url", webhook_url, width=30).pack()

    move_speed = tk.IntVar()
    tk.Label(root, text="Move speed:").pack()
    ValidatedEntry(root, lambda p: p != "" and is_int(p), "move_speed", move_speed, width=10).pack()


def gui():
    root = tk.Tk()
    root.geometry("500x300")
    root.title("Stumpy Macro")
    tab_control = ttk.Notebook(root)

    gather_tab = ttk.Frame(tab_control)
    collect_tab = ttk.Frame(tab_control)
    settings_tab = ttk.Frame(tab_control)

    tab_control.add(gather_tab, text='Gather')
    tab_control.add(collect_tab, text='Collect')
    tab_control.add(settings_tab, text='Settings')
    tab_control.pack(expand=1, fill="both")
    gather_tab_gui(gather_tab)
    collect_tab_gui(collect_tab)
    settings_tab_gui(settings_tab)

    root.mainloop()
