# PATH UTILS
import os
import sys
dir = os.path.dirname(__file__)
KITTY_PY_VER_FILE = f"{dir}/.kittyenv"
KITTY_PY_ENV_DIR = f"{dir}/.kenv"
KITTY_GET_PIP = f"{dir}/get-pip.py"


if os.path.exists(KITTY_PY_VER_FILE):
    with open(KITTY_PY_VER_FILE) as f:
        version = f.read().strip()
else:
    import subprocess
    subprocess.run([ "python3", "-m", "venv", KITTY_PY_ENV_DIR])
    v = subprocess.check_output([f"{KITTY_PY_ENV_DIR}/bin/python", 
                        "-c", 
                        "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"])
    version = v.decode().strip()
    with open(KITTY_PY_VER_FILE, "w") as f:
        f.write(version)


kenv = f"{dir}/.kenv/lib/python{version}"
sys.path.extend([f"{kenv}/lib", f"{kenv}/site-packages", f"{kenv}/dist-packages"])

# PATH UTILS


import datetime
from kitty.fast_data_types import Screen, get_options
from kitty.tab_bar import (
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_tab_with_powerline,
)
from kitty.utils import color_as_int

opts = get_options()

try:
    import psutil
except:
    import subprocess
    subprocess.run([f"{dir}/.kenv/bin/pip", "install", "psutil"]) 
    import psutil
    



BATTERY_FG = as_rgb(int("ffffff", 16))
BATTERY_BG = as_rgb(color_as_int(opts.color4))
CLOCK_FG = as_rgb(int("ffffff", 16))
CLOCK_BG = as_rgb(color_as_int(opts.color4))
DATE_FG = as_rgb(int("ffffff", 16))
DATE_BG = as_rgb(color_as_int(opts.color4))


def _draw_right_status(screen: Screen, is_last: bool) -> int:
    if not is_last:
        return screen.cursor.x
    bat = psutil.sensors_battery()
    battery = "󰂄" 
    if not bat.power_plugged:
        if bat.percent >= 80: battery = f"󰂀"
        elif bat.percent >= 50: battery = "󰁿"
        elif bat.percent >= 30: battery = "󰁾"
        else: battery = "󰁺"
    battery = f"{battery} {bat.percent:.0f}%"
    cells = [
        (BATTERY_BG, screen.cursor.bg, ""),
        (BATTERY_FG, BATTERY_BG, f" {battery} "),

        #(CLOCK_BG, screen.cursor.bg, ""),
        (CLOCK_FG, CLOCK_BG, datetime.datetime.now().strftime("  %H:%M ")),

        (DATE_FG, DATE_BG, datetime.datetime.now().strftime("  %Y/%m/%d ")),
    ]

    right_status_length = 0
    for _, _, cell in cells:
        right_status_length += len(cell)

    draw_spaces = screen.columns - screen.cursor.x - right_status_length
    if draw_spaces > 0:
        screen.draw(" " * draw_spaces)

    for fg, bg, cell in cells:
        screen.cursor.fg = fg
        screen.cursor.bg = bg
        screen.draw(cell)
    screen.cursor.fg = 0
    screen.cursor.bg = 0

    screen.cursor.x = max(screen.cursor.x, screen.columns - right_status_length)
    return screen.cursor.x


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    end = draw_tab_with_powerline(
        draw_data, screen, tab, before, max_title_length, index, is_last, extra_data
    )
    _draw_right_status(
        screen,
        is_last,
    )
    return end



