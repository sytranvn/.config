import subprocess
import platform
import os
import shutil
from kitty.types import run_once
from functools import lru_cache

dir = os.path.dirname(__file__)
spotify_path = f"{dir}/.spotify"


@run_once
def get_npc():
    return shutil.which("nowplaying-cli") or shutil.which("/opt/homebrew/bin/nowplaying-cli")


@lru_cache(maxsize=1)
def get_song(d):
    if platform.system() == 'Darwin':
        npc = get_npc()
        if npc and npc:
            song = subprocess.check_output([npc, "get", "title"]).decode().strip()
            if song == "null":
                return ""
            return song
        else:
            return ""
    else:
        return get_ubuntu_song()


def get_ubuntu_song():
    import psutil

    dbuspid_path = f"{dir}/.dbpid"
    cmd = ["python3", f"{dir}/music.py"]
    if os.path.exists(dbuspid_path):
        with open(dbuspid_path, "r") as f:
            try:
                p = psutil.Process(int(f.read()))
                if p.cmdline() == cmd:
                    # TODO: check actual process status to determine if we kill
                    # or resume it
                    # $ ps <PID>
                    # currently seeing Ss is sleeping status but it still
                    # triggered by event
                    # if p.status() in ('sleeping', 'stopped'):
                    #     from signal import SIGTERM
                    #     p.send_signal(SIGTERM)
                    if os.path.exists(spotify_path):
                        song = open(spotify_path, "r").read()
                        return song
            except psutil.NoSuchProcess:
                pass

    p = subprocess.Popen(
        cmd, start_new_session=True)
    with open(dbuspid_path, "w") as f:
        f.write(str(p.pid))


def start_dbus_monitor():
    import dbus
    from dbus.mainloop.glib import DBusGMainLoop
    from gi.repository import GLib  # noqua

    def notifications(_, message):
        args = message.get_args_list()
        if args[0] == "Spotify":
            with open(spotify_path, "w") as f:
                f.write(str(args[3]))

    DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    bus.add_match_string_non_blocking(
        "eavesdrop=true, interface='org.freedesktop.Notifications', "
        "member='Notify'")
    bus.add_message_filter(notifications)

    mainloop = GLib.MainLoop()
    mainloop.run()


def get_playing_song():
    song = ""
    try:
        meta = subprocess.check_output(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify "
            "/org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get "
            "string:org.mpris.MediaPlayer2.Player string:Metadata".split())
        lines = meta.splitlines()
        entry_line = next(
            (lines[i+1] for i in range(len(lines))
             if b"xesam:title" in lines[i]),
            None
        )
        if entry_line:
            import re
            song = re.search('"(.*)"', entry_line.decode()).group(1)
    except Exception:
        ...
    with open(spotify_path, "w") as f:
        f.write(song)


if __name__ == "__main__":
    get_playing_song()
    start_dbus_monitor()
