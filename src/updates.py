import requests

REPO = "Redfourk/FileLauncher"
LATEST_RELEASE_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

def get_latest_version():
    response = requests.get(LATEST_RELEASE_URL)
    return response.json()["tag_name"]
