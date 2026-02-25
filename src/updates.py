import os
import sys
import subprocess
import requests

# --- CONFIGURATION ---
REPO_PATH = "/Redfourk/FileLauncher"
CURRENT_VERSION = "0.0.0"

def check_for_updates():
    print(f"Current version: {CURRENT_VERSION}. Checking for updates...")
    url = f"https://api.github.com/repos{REPO_PATH}/releases/latest"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print("No releases found.")
            return
        response.raise_for_status()
        data = response.json()
        latest_version = data['tag_name']
        if latest_version > CURRENT_VERSION:
            print(f"New version {latest_version} available!")
            asset = next((a for a in data['assets'] if a['name'].endswith('.exe')), None)
            if not asset:
                print("No .exe found in the latest release.")
                return
            download_update(asset['browser_download_url'])
        else:
            print("You are already using the latest version.")
    except Exception as e:
        print(f"Update check failed: {e}")
def download_update(download_url):
    temp_new_exe = "update_temp.exe"
    print("Downloading update...")
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(temp_new_exe, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    apply_restart_logic(temp_new_exe)
def apply_restart_logic(new_file):
    old_file = sys.executable
    batch_script = "update_swap.bat"
    with open(batch_script, "w") as f:
        f.writelines([
            "@echo off\n",
            "timeout /t 2 /nobreak > nul\n",
            f"del /f /q \"{old_file}\"\n",
            f"move \"{new_file}\" \"{old_file}\"\n",
            f"start \"\" \"{old_file}\"\n",
            "del \"%~f0\"\n"
        ])

    print("Restarting to apply update...")
    subprocess.Popen([batch_script], shell=True)
    sys.exit()


if __name__ == "__main__":
    check_for_updates()
