import sys
from typing import Dict, List
from kitty.boss import Boss
from kittens.tui.loop import debug
from kittens.tui.utils import kitty_opts
from kitty.fast_data_types import get_boss
from kitty.options.utils import KeyMap
# in main, STDIN is for the kitten process and will contain
# the contents of the screen

def main(args: List[str]) -> str:
    # this is the main entry point of the kitten, it will be executed in
    # the overlay window when the kitten is launched
    # whatever this function returns will be available in the
    # handle_result() function
    # KeyMap = Dickt[SingleKey, str]
    keymap: KeyMap = kitty_opts().keymap.copy()
    key, func = list(keymap.items())[0]
    print(f'defined_with_kitty_mod {key.defined_with_kitty_mod}')
    print(f'is_native {key.is_native}')
    print(f'key {key.key}')
    print(f'mods {key.mods}')
    print(f'resolve_kitty_mod {key.resolve_kitty_mod}')
    pretty_keymap = format_keymap(keymap)
    input("Search key: ")
    return ""

def handle_result(args: List[str], answer: str, target_window_id: int, boss: Boss) -> None:
    pass

def format_keymap(keymap: Dict):
    pass 

def format_key(single_key):
    # @properties
    # key
    # mods
    # resolve_kitty_mod
    pass 
