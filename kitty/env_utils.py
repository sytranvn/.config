# CREATE VENV FOR LINUX ONLY
import os
import sys
import platform
dir = os.path.dirname(__file__)
KITTY_PY_VER_FILE = f"{dir}/.kittyenv"
KITTY_PY_ENV_DIR = f"{dir}/.kenv"
KITTY_GET_PIP = f"{dir}/get-pip.py"

if platform.system() != 'Darwin':
    if os.path.exists(KITTY_PY_VER_FILE):
        with open(KITTY_PY_VER_FILE) as f:
            version = f.read().strip()
    else:
        import subprocess
        subprocess.run(["python3", "-m", "venv", KITTY_PY_ENV_DIR])
        v = subprocess.check_output([
            f"{KITTY_PY_ENV_DIR}/bin/python",
            "-c",
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        ])
        version = v.decode().strip()
        with open(KITTY_PY_VER_FILE, "w") as f:
            f.write(version)

    kenv = f"{dir}/.kenv/lib/python{version}"
    sys.path.extend([f"{kenv}/lib", f"{kenv}/site-packages", f"{kenv}/dist-packages"])
