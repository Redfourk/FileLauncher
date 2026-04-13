import ctypes
import platform
import sys
import os
import webbrowser
import pickle

from PyInstaller.utils.conftest import script_dir
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Altering local imports based on OS.
if platform.system() == "Windows":
    from src.prompt import app_version
    from src.gui.netman import check_adapter_status
elif platform.system() == "Linux":
    from prompt import app_version
    from netman import check_adapter_status

from check_repo import get_latest_version

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

# Project Versioning:
project_version = "0.1.0-test.3"
update_status = "You're on the latest version!"

root = tk.Tk()
root.withdraw()

fl = tk.Toplevel(root)
fl.overrideredirect(True)




fl = tk.Toplevel(root)
fl.overrideredirect(True)

# All the fixing of app to not work like a TopLevel cuz of the fact it has a custom style
# Update: I added Multiplatform "Taskbar" Support
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
            print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Successfully Loaded GUI App into Taskbar")
        except Exception as e:
            print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "[WARN]: Could not load GUI App into Taskbar: {e}")
    elif platform.system() == "Linux":
        window.deiconify()
        print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Successfully Loaded GUI App in side bar.")

fl.after(100, lambda: show_in_taskbar(fl))


def close_app():
    root.destroy()

# Begin Google Auth
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/userinfo.profile']

def run_google_auth():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('src/gui/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=58008)
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    return creds



# Check if the User's account is allowlisted
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
assets_dir = current_dir.parent / "assets"

# 2. Open each size
ico16 = Image.open(assets_dir / "FileLauncher16.ico")
ico32 = Image.open(assets_dir / "FileLauncher32.ico")
ico48 = Image.open(assets_dir / "FileLauncher48.ico")
ico256 = Image.open(assets_dir / "FileLauncher256.ico")
ico256.save("FileLauncher.ico", format="ICO",
            append_images=[ico48, ico32, ico16])
icon_path = Path(__file__).parent.parent.parent / "src" / "gui" / "FileLauncher.ico"
prompt_icon_image = Image.open(icon_path)
photo = ImageTk.PhotoImage(prompt_icon_image)
fl.wm_iconphoto(False, photo)

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










close_btn = tk.Button(title_bar, text="r", font=("Marlett", 10),  # 'r' is 'X' in Marlett font
                      width=2, height=1, bg=WIN95_GRAY, relief="raised",
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

from PIL import Image, ImageTk

# 1. Get the path to your 16x16 .ico asset
# (Adjust the path to match your src/assets structure)
assets_dir = Path(__file__).parent.resolve().parent / "assets"
icon_path_16 = assets_dir / "FileLauncher16.ico"

# 2. Open the .ico and convert it to a Tkinter-compatible image
# We keep a reference (header_icon) so it doesn't disappear (garbage collection)
img_open = Image.open(icon_path_16)
header_icon = ImageTk.PhotoImage(img_open)

# 3. Create the Icon Label in the Title Bar
# Note: Win95 icons in the title bar are usually 16x16
icon_label = tk.Label(title_bar, image=header_icon, bg=TITLE_BLUE)
icon_label.image = header_icon # Double-check reference
icon_label.pack(side="left", padx=(3, 2)) # 3px left margin, 2px space before text

# 4. Your existing Title Label (adjusting padding to fit next to icon)
title_label = tk.Label(title_bar, text="FileLauncher",
                       bg=TITLE_BLUE, fg=TEXT_WHITE,
                       font=("MS Sans Serif", 8, "bold"))
title_label.pack(side="left")



WIN95_GRAY = "#c0c0c0"
WIN95_FONT = ("MS Sans Serif", 8)
WIN95_BOLD_FONT = font.Font(family="MS Sans Serif", size=8, weight="bold", )

btn_options_graphical = {
    "bg": WIN95_GRAY,
    "font": WIN95_FONT,
    "relief": "raised",
    "borderwidth": 2,
    "activebackground": "#d9d9d9",
}

btn_options_command_line = {
    "bg": WIN95_GRAY,
    "font": WIN95_FONT,
    "relief": "raised",
    "borderwidth": 2,
    "activebackground": "#d9d9d9",
}


fl.style.configure("Tab", focuscolor=WIN95_GRAY)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TAB CONTENTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERAL TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# General Title
general_content_title = ttk.Label(general, background=WIN95_GRAY, text="General: ", anchor="w", justify="left", font=WIN95_BOLD_FONT)
general_content_title.pack(pady=10, padx=20, fill="x")

# File Status Text

file_status = "Not Selected"

general_content_file_status = ttk.Label(general, text="File Status: " + file_status, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_file_status.pack(pady=5, padx=20, fill="x")

# Network Status Text

# Cross Platform netman process
try:
    network_status = check_adapter_status()
    if platform.system() == "Windows":
        print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Found Network Information")
    elif platform.system() == "Linux":
        print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Found Network Information")
except Exception as e:
    if platform.system() == "Windows":
        print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "[WARN]: " + "Could not find network Information: " + e)
    elif platform.system() == "Linux":
        print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "[WARN]: " + "Could not find network information: " + e)

general_content_network_status = ttk.Label(general, text="Network Status: " + network_status, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_network_status.pack(pady=5, padx=20, fill="x")

# Progress Bar

process_name = " "

# PBar Task Label:
general_content_progress_bar_text = ttk.Label(general, text=process_name, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_progress_bar_text.pack(pady=5, padx=20, fill="x")

# Visual Bar:
general_content_progress_bar = ttk.Progressbar(general, orient="horizontal", length=300, mode="determinate")
general_content_progress_bar.pack(pady=5, padx=10, anchor="w")

# Progress Bar Test Task:
def start_task():
    general_content_progress_bar['value'] = 0
    process_name = "Test Process:"
    general_content_progress_bar_text.config(text=process_name)
    for i in range(5):
        time.sleep(1)
        general_content_progress_bar['value'] += 20
        general.update_idletasks()
    time.sleep(1)
    process_name = " "
    general_content_progress_bar_text.config(text=process_name)


# Progress Bar Test Button:
btn = tk.Button(general, text="Test Pbar", command=start_task)
btn.pack()

def close_app():
    fl.destroy()
    root.destroy()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~USER TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# User Tab Title
user_content_title = ttk.Label(user, background=WIN95_GRAY, text="User Profile: ", anchor="w", justify="left", font=WIN95_BOLD_FONT)
user_content_title.pack(pady=10, padx=20, fill="x")

# Profile Sub-Frame (Sunken look)
user_profile_box = tk.Frame(user, bg=WIN95_GRAY, relief="sunken", borderwidth=2)
user_profile_box.pack(pady=10, padx=20, fill="x")

# Profile Picture Placeholder
user_pfp_canvas = tk.Canvas(user_profile_box, width=80, height=80, bg="#808080", highlightthickness=1, highlightbackground="black")
user_pfp_canvas.grid(row=0, column=0, padx=10, pady=10)
user_pfp_canvas.create_text(40, 40, text="?", fill="white", font=("Courier", 24, "bold"))

# Info Area (Right of PFP)
user_info_frame = tk.Frame(user_profile_box, bg=WIN95_GRAY)
user_info_frame.grid(row=0, column=1, sticky="nw", pady=10)

user_email_text = tk.Label(user_info_frame, text="Account: Not Signed In", bg=WIN95_GRAY, font=WIN95_FONT)
user_email_text.pack(anchor="w")

user_status_text = tk.Label(user_info_frame, text="Status: [UNAUTHORIZED]", bg=WIN95_GRAY, fg="red", font=WIN95_FONT)
user_status_text.pack(anchor="w")

# Update User Tab after Login
def update_user_tab(email, pfp_url=None):
    user_email_text.config(text=f"Account: {email}")
    user_status_text.config(text=f"Status [AUTHORIZED]", fg="green")
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
            user_pfp_canvas.image = photo  # Mandatory reference keep-alive
        except Exception as e:
            print(f"PFP Error: {e}")

    # Future import pfp code

# Auth Button and Function

# Auth Function
def handle_auth_toggle():
    user_status_text.config(text="Status: [CONNECTING...]", fg="blue")
    fl.update()
    try:
        # 2. Call your OAuth logic (we'll define this next)
        creds = run_google_auth()

        if creds:
            # 3. Get user info
            from googleapiclient.discovery import build
            service = build('oauth2', 'v2', credentials=creds)
            info = service.userinfo().get().execute()

            email = info.get('email')
            pfp_url = info.get('picture')

            if check_whitelist(email):
                update_user_tab(email, pfp_url)
                messagebox.showinfo("Access Granted", f"Welcome, {email}!", parent=fl)
            else:
                user_status_text.config(text="Status: [DENIED", fg="red")
                messagebox.showerror("Access Denied", "This account is not authorized to use FileLauncher.", parent=fl)

            update_user_tab(email, pfp_url)
            messagebox.showinfo("Success", f"Welcome, {email}!", parent=fl)
    except Exception as e:
        user_status_text.config(text="Status: [ERROR]", fg="red")
        messagebox.showerror("Auth Error", str(e), parent=fl)

user_auth_btn = tk.Button(user, text="Sign in with Google", command=handle_auth_toggle, **btn_options_graphical)
user_auth_btn.pack(pady=20)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~NETWORK TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Network Tab Title:
network_content_title = ttk.Label(network, background=WIN95_GRAY, text="Network and Service Accessibility:", anchor="w", justify="left", font=WIN95_BOLD_FONT)
network_content_title.pack(pady=10, padx=20, fill="x")

# Service Statuses Indent Box:
network_service_status_box = tk.Frame(network, bg=WIN95_GRAY, relief="sunken", borderwidth=2)
network_service_status_box.pack(pady=10, padx=20, fill="x")

network_service_status_box_frame = tk.Frame(network_service_status_box, bg=WIN95_GRAY)
network_service_status_box_frame.grid(row=0, column=1, sticky="nw", pady=10)

# Network File Server Name:
network_file_server_name = tk.Label(network_service_status_box_frame, text="Current File Server: ", bg=WIN95_GRAY, font=WIN95_FONT)
network_file_server_name.pack(anchor="w")

def ping_server(server_domain):
    url = f"https://{server_domain}"
    try:
        response = requests.head(url, timeout=5)
        if response.status_code < 400:
            print(response.status_code)
            print("Domain is reachable")
            return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach {server_domain}: {e}")
        return False



network_file_server_ping_button = tk.Button(network_service_status_box_frame, text="Ping", bg=WIN95_GRAY, font=WIN95_FONT, command=ping_server("4pepbfihxmsc.shares.zrok.io/health:58008"))
network_file_server_ping_button.pack(anchor="e")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPLOAD TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Upload Tab Title:
upload_content_title = ttk.Label(upload, background=WIN95_GRAY, text="Upload: ", anchor="w", justify="left", font=WIN95_BOLD_FONT)
upload_content_title.pack(pady=10, padx=20, fill="x")

# Upload Text:
upload_button_text = ttk.Label(upload, background=WIN95_GRAY, text="Click the button below to upload a file: ", anchor="w", justify="left", font=WIN95_FONT)
upload_button_text.pack(pady=10, padx=20, fill="x")

# Upload Function:

def show_loading_popup(task):
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)  # No modern title bar
    popup.configure(bg="#c0c0c0", bd=2, relief="raised")
    w, h = 300, 100
    x = (popup.winfo_screenwidth() // 2) - (w // 2)
    y = (popup.winfo_screenheight() // 2) - (h // 2)
    popup.geometry(f"{w}x{h}+{x}+{y}")
    fake_title = tk.Frame(popup, bg="#000080", height=20)
    fake_title.pack(fill="x")
    tk.Label(fake_title, text=task, bg="#000080", fg="white",
             font=("MS Sans Serif", 8, "bold")).pack(side="left", padx=5)
    tk.Label(popup, text="Please wait...", bg="#c0c0c0", font=("MS Sans Serif", 8)).pack(pady=10)
    progress = ttk.Progressbar(popup, orient="horizontal", length=250, mode="determinate")
    progress.pack(pady=5)
    popup.update()
    return popup, progress

def process_file_with_popup():
    source_path = filedialog.askopenfilename(parent=fl, title="Select File")
    if not source_path:
        return
    popup, bar = show_loading_popup("File Upload")
    try:
        UPLOAD_DIR = Path(__file__).parent.resolve() / "uploads"
        if UPLOAD_DIR.exists():
            try:
                for item in UPLOAD_DIR.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                print("Uploads folder purged.")
            except Exception as e:
                print(f"Cleanup error: {e}")
        filename = Path(source_path).name
        dest_path = UPLOAD_DIR / filename
        for i in range(1, 11):
            time.sleep(0.1)
            bar['value'] = i * 10
            popup.update()
        shutil.copy2(source_path, dest_path)
        general_content_file_status.config(text="File Status: Selected")
        popup.destroy()
        messagebox.showinfo("Success", f"Stored {filename} in uploads folder.", parent=fl)
    except Exception as e:
        popup.destroy()
        messagebox.showerror("Error", f"Upload failed: {e}", parent=fl)


# Upload Button:

upload_button = tk.Button(upload, text="Upload File", command=process_file_with_popup, font=WIN95_FONT, justify="left")
upload_button.pack(pady=10, padx=10, anchor="w")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MORE TAB~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# More.. Content Title:
more_content_title = ttk.Label(more, background=WIN95_GRAY, text="Additional Options and Info: ", anchor="w", justify="left", font=WIN95_BOLD_FONT)
more_content_title.pack(pady=10, padx=20, fill="x")

# Project Version:
more_project_version = ttk.Label(more, background=WIN95_GRAY, text="Current App Version:    " + project_version, anchor="w", justify="left", font=WIN95_FONT)
more_project_version.pack(pady=10, padx=20, fill="x")

# Updates Avaliable:

repo_version = get_latest_version("Redfourk", "FileLauncher")

if repo_version > project_version:
    update_status = "There is a new version available. You have " + project_version + " and the \nnewest version is " + repo_version
elif repo_version == project_version:
    update_status = "You are on the latest version! (" + project_version + ")"

more_update_ability = ttk.Label(more, background=WIN95_GRAY, text="Updates Status:   " + update_status, anchor="w", justify="left", font=WIN95_BOLD_FONT)
more_update_ability.pack(pady=10, padx=20, fill="x")

# Repo Link:
more_repo_link_desc = ttk.Label(more, background=WIN95_GRAY, text="Repo Link: ", anchor="w", justify="left", font=WIN95_FONT)
more_repo_link_desc.pack(pady=10, padx=20, fill="x")

def open_github():
    webbrowser.open("https://github.com/Redfourk/FileLauncher")
github_icon_path = str(current_dir / "github_icon.png")
more_gh_icon = tk.PhotoImage(file=github_icon_path, format="PNG", width=64, height=64)

more_link_button = tk.Button(more, image=str(more_gh_icon), command=open_github, cursor="hand2", borderwidth=0, highlightthickness=0)
more_link_button.pack(pady=10, padx=20, anchor="w")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~GitHub Actions Verification~~~~~~~~~~~~~~~
if os.getenv("GITHUB_ACTIONS") == "true":
    print("CI detected: GUI loaded successfully. Exiting.")
    sys.exit(0)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
root.mainloop()
