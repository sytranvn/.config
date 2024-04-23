import subprocess
import platform
import os
from datetime import datetime

dir = os.path.dirname(__file__)
def get_song():
    if platform.system() == 'Darwin':
        if not os.path.exists(f"{dir}/.spotify") or datetime.now().timestamp() - os.stat(f"{dir}/.spotify").st_mtime < 10:
            with open(f"{dir}/.spotify", "r") as f:
                return f.read().rstrip()
        else:
            song = subprocess.check_output(f"osascript {dir}/osx_status.script".split()).decode()
            with open(f"{dir}/.spotify", "w") as f:
                f.write(song)

        return open(f"{dir}/.spotify", "r").read()

