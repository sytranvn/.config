import sys
from typing import List
from kitty.boss import Boss
from kittens.tui.loop import debug
from kittens.tui.utils import kitty_opts
# in main, STDIN is for the kitten process and will contain
# the contents of the screen

def main(args: List[str]) -> str:
    # this is the main entry point of the kitten, it will be executed in
    # the overlay window when the kitten is launched
    # whatever this function returns will be available in the
    # handle_result() function
    keymap = kitty_opts().keymap.copy()
    print(type( keymap))
    input("Search key: ")
    return ""

def handle_result(args: List[str], answer: str, target_window_id: int, boss: Boss) -> None:
    # get the kitty window into which to paste answer
    w = boss.window_id_map.get(target_window_id)
