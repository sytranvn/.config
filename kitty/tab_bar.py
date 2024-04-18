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


def sensors_battery():
    """Return battery information.
    Implementation note: it appears /sys/class/power_supply/BAT0/
    directory structure may vary and provide files with the same
    meaning but under different names, see:
    https://github.com/giampaolo/psutil/issues/966.
    """

    POWER_SUPPLY_PATH = "/sys/class/power_supply"
    null = object()

    def multi_bcat(*paths):
        """Attempt to read the content of multiple files which may
        not exist. If none of them exist return None.
        """
        for path in paths:
            ret = bcat(path, fallback=null)
            if ret != null:
                try:
                    return int(ret)
                except ValueError:
                    return ret.strip()
        return None

    bats = [
        x
        for x in os.listdir(POWER_SUPPLY_PATH)
        if x.startswith('BAT') or 'battery' in x.lower()
    ]
    if not bats:
        return None
    # Get the first available battery. Usually this is "BAT0", except
    # some rare exceptions:
    # https://github.com/giampaolo/psutil/issues/1238
    root = os.path.join(POWER_SUPPLY_PATH, sorted(bats)[0])

    # Base metrics.
    energy_now = multi_bcat(root + "/energy_now", root + "/charge_now")
    power_now = multi_bcat(root + "/power_now", root + "/current_now")
    energy_full = multi_bcat(root + "/energy_full", root + "/charge_full")
    time_to_empty = multi_bcat(root + "/time_to_empty_now")

    # Percent. If we have energy_full the percentage will be more
    # accurate compared to reading /capacity file (float vs. int).
    if energy_full is not None and energy_now is not None:
        try:
            percent = 100.0 * energy_now / energy_full
        except ZeroDivisionError:
            percent = 0.0
    else:
        percent = int(cat(root + "/capacity", fallback=-1))
        if percent == -1:
            return None

    # Is AC power cable plugged in?
    # Note: AC0 is not always available and sometimes (e.g. CentOS7)
    # it's called "AC".
    power_plugged = None
    online = multi_bcat(
        os.path.join(POWER_SUPPLY_PATH, "AC0/online"),
        os.path.join(POWER_SUPPLY_PATH, "AC/online"),
    )
    if online is not None:
        power_plugged = online == 1
    else:
        status = cat(root + "/status", fallback="").strip().lower()
        if status == "discharging":
            power_plugged = False
        elif status in ("charging", "full"):
            power_plugged = True

    # Seconds left.
    # Note to self: we may also calculate the charging ETA as per:
    # https://github.com/thialfihar/dotfiles/blob/
    #     013937745fd9050c30146290e8f963d65c0179e6/bin/battery.py#L55
    if power_plugged:
        secsleft = _common.POWER_TIME_UNLIMITED
    elif energy_now is not None and power_now is not None:
        try:
            secsleft = int(energy_now / power_now * 3600)
        except ZeroDivisionError:
            secsleft = _common.POWER_TIME_UNKNOWN
    elif time_to_empty is not None:
        secsleft = int(time_to_empty * 60)
        if secsleft < 0:
            secsleft = _common.POWER_TIME_UNKNOWN
    else:
        secsleft = _common.POWER_TIME_UNKNOWN

    return _common.sbattery(percent, secsleft, power_plugged)
