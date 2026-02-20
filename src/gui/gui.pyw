import ctypes
import sys
import netman
from src.gui.netman import check_adapter_status

if sys.platform.startswith("win"):
    my_app_id = 'Redfourk.FileLauncher.0.1.0.gui'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

import time
import tkinter
import tkinter as tk
from tkinter import ttk, font
import importlib
import os
from pathlib import Path
import src


root = tk.Tk()
root.withdraw()




fl = tk.Toplevel(root)
fl.overrideredirect(True)


def show_in_taskbar(window):
    # This snippet "re-parents" the window to the taskbar handler
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080

    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # Re-map the window to update the taskbar
    window.withdraw()
    window.after(10, window.deiconify)


# Call it after the window is drawn
fl.after(100, lambda: show_in_taskbar(fl))


def close_app():
    fl.destroy()

from PIL import Image
from pathlib import Path

current_dir = Path(__file__).parent.resolve()
# 1. Define your assets path (adjust based on where you run this)
assets_dir = current_dir.parent / "assets"

# 2. Open each size
ico16 = Image.open(assets_dir / "FileLauncher16.ico")
ico32 = Image.open(assets_dir / "FileLauncher32.ico")
ico48 = Image.open(assets_dir / "FileLauncher48.ico")
ico256 = Image.open(assets_dir / "FileLauncher256.ico")

# 3. Save as a multi-resolution ICO in your main folder
ico256.save("FileLauncher.ico", format="ICO",
            append_images=[ico48, ico32, ico16])

icon_path = Path(__file__).parent.parent.parent / "src" / "gui" / "FileLauncher.ico"

fl.iconbitmap(str(icon_path))
print("Master FileLauncher.ico created!")


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







def close_app():
    root.destroy()


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


# General Tab content:

# General Title
general_content_title = ttk.Label(general, background=WIN95_GRAY, text="General: ", anchor="w", justify="left", font=WIN95_BOLD_FONT)
general_content_title.pack(pady=10, padx=20, fill="x")

# File Status Text

file_status = "Not Selected"

general_content_file_status = ttk.Label(general, text="File Status: " + file_status, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_file_status.pack(pady=5, padx=20, fill="x")

# Network Status Text

network_status = check_adapter_status()

general_content_network_status = ttk.Label(general, text="Network Status: " + network_status, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_network_status.pack(pady=5, padx=20, fill="x")

# Progress Bar

process_name = " "

general_content_progress_bar_text = ttk.Label(general, text=process_name, background=WIN95_GRAY, anchor="w", justify="left", font=WIN95_FONT)
general_content_progress_bar_text.pack(pady=5, padx=20, fill="x")


general_content_progress_bar = ttk.Progressbar(general, orient="horizontal", length=300, mode="determinate")
general_content_progress_bar.pack(pady=5, padx=10, anchor="w")

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

btn = tk.Button(general, text="Test Pbar", command=start_task)
btn.pack()

root.mainloop()