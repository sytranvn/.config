from datetime import datetime
from os.path import dirname, exists, stat
import platform


def get_linux_bat():
    try:
        import psutil
    except Exception:
        import subprocess

        subprocess.run([f"{dir}/.kenv/bin/pip", "install", "psutil"])
        import psutil

    return psutil.sensors_battery()


class Battery:
    def __init__(self, percent, power_plugged) -> None:
        self.power_plugged = power_plugged
        self.percent = percent


def get_macos_bat():

    from threading import Thread
    import os

    def _get_bat():
        import re
        from subprocess import check_output

        b = check_output("pmset -g batt".split(" ")).decode()
        percent = re.search("(\\d+)%", b).group(1)
        pwer_plugged = "AC attached;" in b

        with open(dirname(__file__) + "/.bat", "w") as f:
            f.write(f"{percent} {pwer_plugged}")
        Battery(int(percent), pwer_plugged)

    if (
        exists(dirname(__file__) + "/.bat")
        and os.stat(dirname(__file__) + "/.bat").st_mtime
        < datetime.now().timestamp() - 60
    ):
        return _get_bat()

    t = Thread(target=_get_bat)
    t.start()
    with open(dirname(__file__) + "/.bat", "r") as f:
        percent, pwer_plugged = f.read().strip().split(" ")

    return Battery(eval(percent), eval(pwer_plugged))


def get_bat():
    if platform.system() == "Darwin":
        bat = get_macos_bat()
    else:
        bat = get_linux_bat()
    battery = "󰂄"

    if not bat.power_plugged:
        if bat.percent >= 80:
            battery = "󰂀"
        elif bat.percent >= 50:
            battery = "󰁿"
        elif bat.percent >= 30:
            battery = "󰁾"
        else:
            battery = "󰁺"
    battery = f"{battery} {bat.percent:.0f}%"
    return battery
