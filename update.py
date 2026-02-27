import requests
import zipfile
import io
import os
import shutil
import sys

# --- CONFIGURATION ---
REPO_OWNER = "Redfourk"
REPO_NAME = "FileLauncher"
# Updated to use your specific test tag
TAG_NAME = "FileLauncher-0.1.0-test.1"

# CORRECTED URL: Added missing slash and used /tags/ instead of /heads/
ZIP_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/archive/refs/tags/0.1.0-test.1.zip"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def update_project():
    try:
        print(f"Connecting to GitHub to download {TAG_NAME}...")
        # timeout added to avoid hanging on restricted networks
        response = requests.get(ZIP_URL, stream=True, timeout=20)
        response.raise_for_status()

        # 1. Load ZIP into memory
        zip_data = zipfile.ZipFile(io.BytesIO(response.content))

        # 2. Extract to a temporary folder
        temp_dir = os.path.join(ROOT_DIR, "_update_temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        zip_data.extractall(temp_dir)

        # 3. Identify the folder inside the ZIP (GitHub tags add the tag name)
        # Usually format is: REPO_NAME-TAG_NAME
        extracted_folder = os.path.join(temp_dir, f"{REPO_NAME}-{TAG_NAME}")

        if not os.path.exists(extracted_folder):
            # Fallback check: GitHub sometimes strips 'v' or prefix from folder names
            extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])

        print("Updating local project files...")
        # 4. Overwrite ROOT_DIR with files from the extracted folder
        for item in os.listdir(extracted_folder):
            source = os.path.join(extracted_folder, item)
            destination = os.path.join(ROOT_DIR, item)

            if os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        # 5. Cleanup
        shutil.rmtree(temp_dir)
        print("\nSUCCESS: Project updated to latest version. Please restart.")
        sys.exit()

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to GitHub. Check your internet or proxy.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    update_project()

