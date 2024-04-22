import platform


def get_linux_bat():
    try:
        import psutil
    except Exception:
        import subprocess
        subprocess.run([f"{dir}/.kenv/bin/pip", "install", "psutil"])
        import psutil

        return psutil.sensors_battery()


class Battery():
    def __init__(self, percent, power_plugged) -> None:
        self.power_plugged = power_plugged
        self.percent = percent


def get_macos_bat():

    from subprocess import check_output
    import re
    b = check_output("pmset -g batt".split(" ")).decode()
    percent = re.search("(\\d+)%", b).group(1)
    pwer_plugged = "AC attached;" in b

    return Battery(int(percent), pwer_plugged)


def get_bat():
    if platform.system() != 'Darwin':
        bat = get_linux_bat()
    else:
        bat = get_macos_bat()
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
