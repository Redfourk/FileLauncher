import os
import subprocess
import sys
import ctypes
from pathlib import Path


if sys.platform.startswith("win"):
    myappid = 'Redfourk.FileLauncher.0.1.0.main'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
def launch():
    current_dir = Path(__file__).parent.resolve()
    target_script = current_dir / "prompt.py"
    python_exe = sys.executable.lower().replace("python.exe", "pythonw.exe")
    try:
        subprocess.Popen(
            [python_exe, str(target_script)],
            close_fds=True,
            start_new_session=True
        )
    except Exception as e:
        subprocess.Popen([sys.executable, str(target_script)])

if __name__ == "__main__":
    launch()
    sys.exit()
