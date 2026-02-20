import os
import subprocess
import sys
import ctypes
from pathlib import Path

# 1. Set the App ID immediately for Taskbar grouping
if sys.platform.startswith("win"):
    myappid = 'Redfourk.FileLauncher.0.1.0.main'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def launch():
    # 2. Find paths relative to this file
    current_dir = Path(__file__).parent.resolve()
    target_script = current_dir / "prompt.py"

    # 3. Use 'pythonw.exe' to hide the black terminal window
    python_exe = sys.executable.lower().replace("python.exe", "pythonw.exe")

    # 4. Use Popen with DETACHED_PROCESS so main.py can exit immediately
    # 0x00000008 is the flag for DETACHED_PROCESS
    try:
        # Remove creationflags=0x00000008
        subprocess.Popen(
            [python_exe, str(target_script)],
            close_fds=True,
            start_new_session=True
        )
    except Exception as e:
        # If pythonw fails, fallback to standard python
        subprocess.Popen([sys.executable, str(target_script)])

if __name__ == "__main__":
    launch()
    # 5. Exit main.py immediately so no background process lingers
    sys.exit()
