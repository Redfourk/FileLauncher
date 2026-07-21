import ctypes
import platform
import subprocess
import sys
import os
import webbrowser
import pickle
import urllib.request
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from io import BytesIO
from PIL import ImageTk

# App Version:
app_version = ("-0.1.0-test.6")

# Altering local imports based on OS.
if platform.system() == "Windows":
    from src.gui.netman import check_adapter_status
elif platform.system() == "Linux":
    from netman import check_adapter_status

from src.updates.check_repo import get_latest_version

# Setting an App ID for Windows.
if sys.platform.startswith("win"):
    my_app_id = 'Redfourk.FileLauncher.0.1.0.gui'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

import shutil
import time
import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
from pathlib import Path
from PIL import Image
import threading

# Project Versioning:
project_version = "0.1.0-test.6"
update_status = "You're on the latest version!"

root = tk.Tk()
root.withdraw()

fl = tk.Toplevel(root)
fl.overrideredirect(True)


def show_in_taskbar(window):
    if platform.system() == "Windows":
        try:
            GWL_EXSTYLE = -20
            WS_EX_APPWINDOW = 0x00040000
            WS_EX_TOOLWINDOW = 0x00000080
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            window.withdraw()
            window.after(10, window.deiconify)
            print(
                f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Successfully Loaded GUI App into Taskbar")
        except Exception as e:
            print(
                f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "[WARN]: Could not load GUI App into Taskbar: {e}")
    elif platform.system() == "Linux":
        window.deiconify()
        print(
            f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Successfully Loaded GUI App in side bar.")


fl.after(100, lambda: show_in_taskbar(fl))


def close_app():
    fl.destroy()
    root.destroy()


# Begin Google Auth
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'openid',
          'https://www.googleapis.com/auth/userinfo.profile']


def run_google_auth():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=58008)
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def check_whitelist(email):
    try:
        current_dir = Path(__file__).parent.resolve()
        src_dir = current_dir.parent.resolve()
        base_dir = src_dir.parent.resolve()
        with open(base_dir / "whitelist.txt", 'r') as f:
            allowed = [line.strip().lower() for line in f.readlines()]
        return email.lower() in allowed
    except Exception as e:
        print(f"{e}")


current_dir = Path(__file__).parent.resolve()
assets_dir = current_dir.parent / "assets" / "icons"
update_dir = current_dir.parent / "updates"

icon_path = Path(__file__).parent.parent.parent / "src" / "gui" / "FileLauncher.ico"
prompt_icon_image = Image.open(icon_path)
photo = ImageTk.PhotoImage(prompt_icon_image)
fl.wm_iconphoto(False, photo)
root.wm_iconphoto(False, photo)

print("[FileLauncher" + app_version + "]: " + "Master FileLauncher.ico created!")

fl.style = ttk.Style()
fl.style.layout("Tab", [
    ('Notebook.tab', {'sticky': 'nswe', 'children': [
        ('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children': [
            ('Notebook.label', {'side': 'top', 'sticky': ''})
        ]})
    ]})
])

fl.style.theme_use('classic')
fl.title("FileLauncher")

fl.update_idletasks()
window_width = 500
window_height = 500
screen_width = fl.winfo_screenwidth()
screen_height = fl.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
fl.geometry(f"{window_width}x{window_height}+{x}+{y}")
fl.configure(bg="#c0c0c0")

TITLE_BLUE = "#000080"
TEXT_WHITE = "#ffffff"
WIN95_GRAY = "#c0c0c0"

title_bar = tk.Frame(fl, bg=TITLE_BLUE, height=20, relief="raised", bd=0)
title_bar.pack(expand=False, fill="x")

close_btn = tk.Button(title_bar, text="r", font=("Marlett", 10), width=2, height=1, bg=WIN95_GRAY, relief="raised",
                      borderwidth=1, command=close_app)
close_btn.pack(side="right", padx=2, pady=2)


def start_move(event):
    fl.x = event.x
    fl.y = event.y


def stop_move(event):
    fl.x = None
    fl.y = None


def moving(event):
    x = (event.x_root - fl.x)
    y = (event.y_root - fl.y)
    fl.geometry(f"+{x}+{y}")


title_bar.bind("<Button-1>", start_move)
title_bar.bind("<ButtonRelease-1>", stop_move)
title_bar.bind("<B1-Motion>", moving)

assets_dir = Path(__file__).parent.resolve().parent / "assets"
icon_path_16 = assets_dir / "icons" / "FileLauncher32.ico"
img_open = Image.open(icon_path_16)
header_icon = ImageTk.PhotoImage(img_open)
icon_label = tk.Label(title_bar, image=header_icon, bg=TITLE_BLUE)
icon_label.image = header_icon
icon_label.pack(side="left", padx=(3, 2))
title_label = tk.Label(title_bar, text="FileLauncher", bg=TITLE_BLUE, fg=TEXT_WHITE, font=("MS Sans Serif", 8, "bold"))
title_label.pack(side="left")

WIN95_FONT = ("MS Sans Serif", 8)
WIN95_BOLD_FONT = font.Font(family="MS Sans Serif", size=8, weight="bold")

btn_options_graphical = {
    "bg": WIN95_GRAY,
    "font": WIN95_FONT,
    "relief": "raised",
    "borderwidth": 2,
    "activebackground": "#d9d9d9",
}

fl.style.configure("Tab", focuscolor=WIN95_GRAY)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TAB CONTENTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

tabs = ttk.Notebook(fl, takefocus=False)
general = tk.Frame(tabs, bg=WIN95_GRAY)
user = tk.Frame(tabs, bg=WIN95_GRAY)
network = tk.Frame(tabs, bg=WIN95_GRAY)
upload = tk.Frame(tabs, bg=WIN95_GRAY)
more = tk.Frame(tabs, bg=WIN95_GRAY)
tabs.add(general, text=" General ")
tabs.add(user, text=" User ")
tabs.add(network, text=" Network ")
tabs.add(upload, text=" Upload ")
tabs.add(more, text=" More... ")
tabs.pack(expand=1, fill="both", padx=5, pady=5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERAL TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

general_content_title = ttk.Label(general, background=WIN95_GRAY, text="General: ", anchor="w", justify="left",
                                  font=WIN95_BOLD_FONT)
general_content_title.pack(pady=10, padx=20, fill="x")

file_status = "Not Selected"
general_content_file_status = ttk.Label(general, text="File Status: " + file_status, background=WIN95_GRAY, anchor="w",
                                        justify="left", font=WIN95_FONT)
general_content_file_status.pack(pady=5, padx=20, fill="x")

try:
    network_status = check_adapter_status()
except Exception as e:
    network_status = "Unavailable"

general_content_network_status = ttk.Label(general, text="Network Status: " + network_status, background=WIN95_GRAY,
                                           anchor="w", justify="left", font=WIN95_FONT)
general_content_network_status.pack(pady=5, padx=20, fill="x")

process_name = " "
general_content_progress_bar_text = ttk.Label(general, text=process_name, background=WIN95_GRAY, anchor="w",
                                              justify="left", font=WIN95_FONT)
general_content_progress_bar_text.pack(pady=5, padx=20, fill="x")

general_content_progress_bar = ttk.Progressbar(general, orient="horizontal", length=300, mode="determinate")
general_content_progress_bar.pack(pady=5, padx=10, anchor="w")


# Shared backend `upload task linked to the progress bar and network settings
def execute_real_upload():
    file_path = filedialog.askopenfilename(parent=fl, title="Select File to Upload")
    if not file_path:
        return

    def upload_worker():
        try:
            general_content_progress_bar['value'] = 0
            general_content_progress_bar_text.config(text="Uploading to Server:")
            ip = ip_entry.get().strip()
            port = port_entry.get().strip()
            url = f"http://{ip}:{port}/upload"

            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            general_content_progress_bar['value'] = 25
            fl.update_idletasks()

            with open(file_path, "rb") as f:
                file_data = f.read()

            general_content_progress_bar['value'] = 60
            fl.update_idletasks()

            headers = {
                'Content-Type': 'application/octet-stream',
                'X-File-Name': filename,
                'Content-Length': str(file_size)
            }

            req = urllib.request.Request(url, data=file_data, headers=headers, method='POST')

            try:
                with urllib.request.urlopen(req) as response:
                    response_body = response.read().decode('utf-8')
                    result_json = json.loads(response_body)

                    general_content_progress_bar['value'] = 100
                    general_content_file_status.config(text=f"File Status: Sent ({filename})")
                    messagebox.showinfo("Success",
                                        f"Server Response: {result_json.get('message', 'Uploaded successfully!')}",
                                        parent=fl)

            except urllib.error.HTTPError as he:
                error_body = he.read().decode('utf-8')
                try:
                    err_json = json.loads(error_body)
                    status = err_json.get('status', 'Error')
                    reason = err_json.get('reason') or err_json.get('message') or error_body
                    server_message = f"Status: {status.upper()}\nReason: {reason}"
                except json.JSONDecodeError:
                    server_message = error_body

                general_content_progress_bar['value'] = 0
                messagebox.showerror("Server Rejected Request", f"Server Error ({he.code}):\n\n{server_message}", parent=fl)

        except Exception as e:
            general_content_progress_bar['value'] = 0
            messagebox.showerror("Connection Error", f"Could not connect to backend:\n{str(e)}", parent=fl)

        finally:
            time.sleep(1)
            general_content_progress_bar_text.config(text=" ")
            general_content_progress_bar['value'] = 0

    threading.Thread(target=upload_worker, daemon=True).start()


btn = tk.Button(general, text="Upload File (Pbar Test)", command=execute_real_upload, **btn_options_graphical)
btn.pack(pady=10)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~USER TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

user_content_title = ttk.Label(user, background=WIN95_GRAY, text="User Profile: ", anchor="w", justify="left",
                               font=WIN95_BOLD_FONT)
user_content_title.pack(pady=10, padx=20, fill="x")

user_profile_box = tk.Frame(user, bg=WIN95_GRAY, relief="sunken", borderwidth=2)
user_profile_box.pack(pady=10, padx=20, fill="x")

user_pfp_canvas = tk.Canvas(user_profile_box, width=80, height=80, bg="#808080", highlightthickness=1,
                            highlightbackground="black")
user_pfp_canvas.grid(row=0, column=0, padx=10, pady=10)
user_pfp_canvas.create_text(40, 40, text="?", fill="white", font=("Courier", 24, "bold"))

user_info_frame = tk.Frame(user_profile_box, bg=WIN95_GRAY)
user_info_frame.grid(row=0, column=1, sticky="nw", pady=10)

user_email_text = tk.Label(user_info_frame, text="Account: Not Signed In", bg=WIN95_GRAY, font=WIN95_FONT)
user_email_text.pack(anchor="w")

user_status_text = tk.Label(user_info_frame, text="Status: [UNAUTHORIZED]", bg=WIN95_GRAY, fg="red", font=WIN95_FONT)
user_status_text.pack(anchor="w")


def update_user_tab(email, pfp_url=None):
    user_email_text.config(text=f"Account: {email}")
    user_status_text.config(text=f"Status: [AUTHORIZED]", fg="green")
    user_auth_btn.config(text="Logout / Disconnect")
    if pfp_url:
        try:
            response = requests.get(pfp_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            user_pfp_canvas.delete("all")
            user_pfp_canvas.create_image(40, 40, image=photo)
            user_pfp_canvas.image = photo
        except Exception as e:
            print(f"PFP Error: {e}")


def handle_auth_toggle():
    user_status_text.config(text="Status: [CONNECTING...]", fg="blue")
    fl.update()
    try:
        creds = run_google_auth()
        if creds:
            from googleapiclient.discovery import build
            service = build('oauth2', 'v2', credentials=creds)
            info = service.userinfo().get().execute()

            email = info.get('email')
            pfp_url = info.get('picture')

            if check_whitelist(email):
                update_user_tab(email, pfp_url)
                messagebox.showinfo("Access Granted", f"Welcome, {email}!", parent=fl)
            else:
                user_status_text.config(text="Status: [DENIED]", fg="red")
                messagebox.showerror("Access Denied", "This account is not authorized to use FileLauncher.", parent=fl)
    except Exception as e:
        user_status_text.config(text="Status: [ERROR]", fg="red")
        messagebox.showerror("Auth Error", str(e), parent=fl)


user_auth_btn = tk.Button(user, text="Sign in with Google", command=handle_auth_toggle, **btn_options_graphical)
user_auth_btn.pack(pady=20)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NETWORK TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

network_content_title = ttk.Label(network, background=WIN95_GRAY, text="Server Connection Settings:", anchor="w",
                                  justify="left", font=WIN95_BOLD_FONT)
network_content_title.pack(pady=10, padx=20, fill="x")

network_service_status_box = tk.Frame(network, bg=WIN95_GRAY, relief="sunken", borderwidth=2)
network_service_status_box.pack(pady=10, padx=20, fill="both", expand=True)

# IP and Port Fields added here
settings_inner_frame = tk.Frame(network_service_status_box, bg=WIN95_GRAY)
settings_inner_frame.pack(pady=20, padx=20, anchor="w")

tk.Label(settings_inner_frame, text="Server IP:", bg=WIN95_GRAY, font=WIN95_FONT).grid(row=0, column=0, sticky="w",
                                                                                       pady=5)
ip_entry = ttk.Entry(settings_inner_frame, width=25)
ip_entry.insert(0, "127.0.0.1")
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(settings_inner_frame, text="Port Number:", bg=WIN95_GRAY, font=WIN95_FONT).grid(row=1, column=0, sticky="w",
                                                                                         pady=5)
port_entry = ttk.Entry(settings_inner_frame, width=25)
port_entry.insert(0, "8080")
port_entry.grid(row=1, column=1, padx=10, pady=5)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPLOAD TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

upload_content_title = ttk.Label(upload, background=WIN95_GRAY, text="Upload: ", anchor="w", justify="left",
                                 font=WIN95_BOLD_FONT)
upload_content_title.pack(pady=10, padx=20, fill="x")

upload_button_text = ttk.Label(upload, background=WIN95_GRAY,
                               text="Click the button below to upload a file to the active server:", anchor="w",
                               justify="left", font=WIN95_FONT)
upload_button_text.pack(pady=10, padx=20, fill="x")

upload_button = tk.Button(upload, text="Upload File", command=execute_real_upload, font=WIN95_FONT)
upload_button.pack(pady=10, padx=20, anchor="w")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MORE TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

more_content_title = ttk.Label(more, background=WIN95_GRAY, text="Additional Options and Info: ", anchor="w",
                               justify="left", font=WIN95_BOLD_FONT)
more_content_title.pack(pady=10, padx=20, fill="x")

more_project_version = ttk.Label(more, background=WIN95_GRAY, text="Current App Version:    " + project_version,
                                 anchor="w", justify="left", font=WIN95_FONT)
more_project_version.pack(pady=10, padx=20, fill="x")

more_update_ability = ttk.Label(more, background=WIN95_GRAY, text="Updates Status:   Checking...", anchor="w",
                                justify="left", font=WIN95_BOLD_FONT)
more_update_ability.pack(pady=10, padx=20, fill="x")

more_repo_link_desc = ttk.Label(more, background=WIN95_GRAY, text="Repo Link: ", anchor="w", justify="left",
                                font=WIN95_FONT)
more_repo_link_desc.pack(pady=10, padx=20, fill="x")


def open_github():
    webbrowser.open("https://github.com/Redfourk/FileLauncher")


github_icon_path = str(assets_dir / "photos" / "github_icon.png")
if os.path.exists(github_icon_path):
    more_gh_icon = tk.PhotoImage(file=github_icon_path, format="PNG", width=64, height=64)
    more_link_button = tk.Button(more, image=more_gh_icon, command=open_github, cursor="hand2", borderwidth=0,
                                 highlightthickness=0, background=WIN95_GRAY)
    more_link_button.pack(pady=10, padx=20, anchor="w")


def trigger_system_update():
    fl.destroy()
    root.destroy()
    updater_popup = tk.Tk()
    updater_popup.overrideredirect(True)
    updater_popup.configure(background='#c0c0c0', bd=2, relief="raised")
    w, h = 300, 100
    x = (updater_popup.winfo_screenwidth() // 2) - (w // 2)
    y = (updater_popup.winfo_screenheight() // 2) - (h // 2)
    updater_popup.geometry(f"{w}x{h}+{x}+{y}")
    fake_title = tk.Frame(updater_popup, bg="#000080", height=20)
    fake_title.pack(fill="x")
    tk.Label(fake_title, text="System Update", bg="#000080", fg="white", font=("MS Sans Serif", 8, "bold")).pack(
        side="left", padx=5)

    tk.Label(updater_popup, text="Applying updates, please wait...", bg="#c0c0c0", font=("MS Sans Serif", 8)).pack(
        pady=10)
    progress = ttk.Progressbar(updater_popup, orient="horizontal", length=250, mode="indeterminate")
    progress.pack(pady=5)
    progress.start(10)
    updater_popup.update()

    try:
        current_file_dir = Path(__file__).parent.resolve()
        root_dir = current_file_dir.parent.parent.resolve()
        updater_script = root_dir / "update.py"
        process = subprocess.Popen([sys.executable, str(updater_script)])
        while process.poll() is None:
            updater_popup.update()
            time.sleep(0.1)
    except Exception as e:
        print(f"Failed to run update.py: {e}")

    updater_popup.destroy()
    sys.exit(0)


more_update_button = tk.Button(more, command=trigger_system_update, text="Update Application", cursor="hand2",
                               font=WIN95_FONT, background=WIN95_GRAY)
more_update_button.pack(pady=10, padx=20, anchor="w")


def check_for_updates_and_toggle_button():
    try:
        repo_version = get_latest_version("Redfourk", "FileLauncher")
        if repo_version > project_version:
            update_status = f"There is a new version available.\nYou have {project_version} and newest is {repo_version}"
            more_update_ability.config(text="Updates Status: " + update_status)
            more_update_button.config(state="normal")
        else:
            update_status = f"You are on the latest version! ({project_version})"
            more_update_ability.config(text="Updates Status: " + update_status)
            more_update_button.config(state="disabled")
    except Exception as e:
        more_update_ability.config(text="Updates Status: Could not check for updates!")
        more_update_button.config(state="normal")


fl.after(100, check_for_updates_and_toggle_button)

if os.getenv("GITHUB_ACTIONS") == "true":
    print("CI detected: GUI loaded successfully. Exiting.")
    sys.exit(0)

root.mainloop()