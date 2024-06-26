import sys
import os

dir = os.path.dirname(__file__)
sys.path.append(dir)

import env_utils  # noqa

from battery import get_bat  # noqa
from music import get_song  # noqa

import datetime  # noqa
from kitty.fast_data_types import Screen, get_options  # noqa
from kitty.tab_bar import (  # noqa
    DrawData,
    ExtraData,
    TabBarData,
    as_rgb,
    draw_tab_with_powerline,
)
from kitty.utils import color_as_int  # noqa

opts = get_options()


SPOTIFY_FG = as_rgb(int("ffffff", 16))
SPOTIFY_BG = as_rgb(int("1DB954", 16))
BATTERY_FG = as_rgb(int("ffffff", 16))
BATTERY_BG = as_rgb(color_as_int(opts.color4))
CLOCK_FG = as_rgb(int("ffffff", 16))
CLOCK_BG = as_rgb(color_as_int(opts.color4))
DATE_FG = as_rgb(int("ffffff", 16))
DATE_BG = as_rgb(color_as_int(opts.color4))


def _draw_right_status(screen: Screen, is_last: bool) -> int:
    if not is_last:
        return screen.cursor.x
    now = datetime.datetime.now()
    cache_now = now.replace(microsecond=0)
    battery = get_bat(cache_now.replace(second=0))
    song = get_song(cache_now)  # get song need to be more agressive

    song = f" {song[:20]}" if song else ""
    # song += int(sum([1 for i in range(len(song)) if song[i] > 'ỿ']) * 0.5) * " "
    song += int(sum([1 for i in range(len(song)) if 'ỿ' < song[i]]) * 1.5) * " " + " "
    cells = [
        (CLOCK_BG, screen.cursor.bg, ""),
        (BATTERY_FG, BATTERY_BG, f"{battery} "),
        (CLOCK_FG, CLOCK_BG, now.strftime("  %H:%M ")),
        (DATE_FG, DATE_BG, now.strftime(" %Y/%-m/%-d ")),
        (SPOTIFY_BG, BATTERY_BG, ""),
        (SPOTIFY_FG, SPOTIFY_BG, f" {song}"),
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
