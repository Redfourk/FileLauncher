import requests
import zipfile
import io
import os
import shutil
import sys

# --- CONFIGURATION ---
REPO_OWNER = "Redfourk"
REPO_NAME = "FileLauncher"
TAG_NAME = "0.1.0-test.2"


ZIP_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/zipball/"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def update_project():
    try:
        print(f"Connecting to GitHub to download {TAG_NAME}...")
        response = requests.get(ZIP_URL, stream=True, timeout=20)
        response.raise_for_status()
        zip_data = zipfile.ZipFile(io.BytesIO(response.content))
        temp_dir = os.path.join(ROOT_DIR, "_update_temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        zip_data.extractall(temp_dir)
        extracted_folder = os.path.join(temp_dir, f"{REPO_NAME}-{TAG_NAME}")

        if not os.path.exists(extracted_folder):
            extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

        print("Updating local project files...")
        for item in os.listdir(extracted_folder):
            source = os.path.join(extracted_folder, item)
            destination = os.path.join(ROOT_DIR, item)

            if os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        shutil.rmtree(temp_dir)
        print("\nSUCCESS: Project updated to latest version. Please restart.")
        sys.exit()

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to GitHub. Check your internet or proxy.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    update_project()

