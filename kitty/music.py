import subprocess
import platform
import os
from datetime import datetime

dir = os.path.dirname(__file__)
def get_song():
    if platform.system() == 'Darwin':
        if os.path.exists(f"{dir}/.spotify"):
            stat = os.stat(f"{dir}/.spotify")
            if datetime.now().timestamp() - stat.st_mtime > 10000:
                with open(f"{dir}/.spotify", "r") as f:
                    return f.read().rstrip()
        else:
            song = subprocess.check_output(f"osascript {dir}/osx_status.script".split()).decode()
            with open(f"{dir}/.spotify", "w") as f:
                f.write(song)

        return open(f"{dir}/.spotify", "r").read()

