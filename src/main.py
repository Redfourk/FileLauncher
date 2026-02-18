import os
import subprocess
import prompt
from pathlib import Path
import sys


# This is the main control script for FileLauncher:
# By Redfourk

print("Welcome to FileLauncher, the fast, user-friendly file transfer program!")
# subprocess.run(["prompt.py"])

current_dir = Path(__file__).parent.resolve()
target_script = current_dir / "prompt.py"

subprocess.run([sys.executable, str(target_script)])



