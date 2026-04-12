import tkinter as tk
import platform
from PIL import Image, ImageTk
import os
system_os = platform.system()

import ctypes
import multiprocessing
from tabnanny import verbose

app_version = "-0.1.0-test.3"

def main():
    import os
    import subprocess
    import sys
    from pathlib import Path

    if sys.platform.startswith("win"):
        myappid = 'Redfourk.FileLauncher.0.1.0.prompt'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    from tkinter import ttk
    base_dir = Path(__file__).parent.resolve()
    icon_path = base_dir / "FileLauncher.ico"

    # GUI Execution code:
    def graphical_button_operation():
        target_script = base_dir / "gui" / "gui.pyw"
        python_exe = sys.executable.lower().replace("python.exe", "pythonw.exe")
        try:
            subprocess.Popen(
                [python_exe, str(target_script)],
                creationflags=0x00000008,
                close_fds=True,
                start_new_session=True,
                cwd=str(base_dir),
            )
            prompt.after(100, close_app)
        except Exception:
            subprocess.Popen([sys.executable, str(target_script)])

    def command_line_button_operation():
        # Reserved for future CLI integration:
        print("This feature is not available yet!")
        # Code will go here:

    # Prompt Tkinter App creation:
    prompt = tk.Tk()

    # Multi-Platform Icon Generation (just kidding, didn't add macOS Support hehe!)
    if system_os == "Windows":
        try:
            prompt.iconbitmap(icon_path)
            print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Prompt App icon Loaded Successfully")
        except Exception as e:
            print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Failed to load Prompt App Icon with Exception: {e}")

    elif system_os == "Linux":
        try:
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            prompt.wm_iconphoto(False, photo)
            # Keep a reference to the photo object so it doesn't get garbage collected
            prompt._icon = photo
            print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Prompt App icon loaded successfully")
        except Exception as e:
            print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Failed to load Prompt App Icon with Exception: {e}")
    prompt.style = ttk.Style()
    prompt.style.theme_use('classic')
    prompt.title("Info")
    width, height = 350, 150
    screen_width = prompt.winfo_screenwidth()
    screen_height = prompt.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    prompt.geometry(f"{width}x{height}+{x}+{y}")
    prompt.configure(bg="#c0c0c0")
    prompt.overrideredirect(True)

    # Multiplatform "Taskbar" Support
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
                print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "Successfully Loaded Prompt App into Taskbar")
            except Exception as e:
                print(f"[FileLauncher" + app_version + "]: " + "[WINDOWS COMPAT MODE]: " + "[WARN]: Could not load Prompt App into Taskbar: {e}")
        elif platform.system() == "Linux":
            window.deiconify()
            print(f"[FileLauncher" + app_version + "]: " + "[LINUX COMPAT MODE]: " + "Successfully Loaded Prompt App in side bar.")

    # Strikethrough Text Effect:
    def strikethrough(text):
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result

    prompt.after(100, lambda: show_in_taskbar(prompt))
    TITLE_BLUE, TEXT_WHITE, WIN95_GRAY = "#000080", "#ffffff", "#c0c0c0"
    WIN95_FONT = ("MS Sans Serif", 8)
    title_bar = tk.Frame(prompt, bg=TITLE_BLUE, height=20, relief="raised", bd=0)
    title_bar.pack(expand=False, fill="x")
    title_label = tk.Label(title_bar, text=" FileLauncher", bg=TITLE_BLUE, fg=TEXT_WHITE,
                           font=("MS Sans Serif", 8, "bold"))
    title_label.pack(side="left")
    def close_app():
        prompt.destroy()
    close_btn = tk.Button(title_bar, text="r", font=("Marlett", 10), width=2, height=1, bg=WIN95_GRAY, relief="raised",
                          borderwidth=1, command=close_app)
    close_btn.pack(side="right", padx=2, pady=2)
    def start_move(event):
        prompt.x, prompt.y = event.x, event.y
    def moving(event):
        x, y = (event.x_root - prompt.x), (event.y_root - prompt.y)
        prompt.geometry(f"+{x}+{y}")
    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", moving)
    tk.Label(prompt,
             text="\nFileLauncher has Graphical User Interface capabilities.\n Would you like to use the GUI, \nor stay in a command line interface?",
             bg="#c0c0c0").pack()
    btn_opts = {"bg": WIN95_GRAY, "font": WIN95_FONT, "relief": "raised", "borderwidth": 2,
                "activebackground": "#d9d9d9"}

    # GUI Button:
    gui = tk.Button(prompt, text="GUI", width=10, command=graphical_button_operation, **btn_opts)
    gui.pack(side="left", padx=10, pady=10)

    # CLI Button:
    tk.Button(prompt, text=strikethrough("COMMAND LINE") + " COMING SOON", width=30, command=command_line_button_operation, **btn_opts).pack(side="right", padx=10, pady=10)


    prompt.mainloop()


if __name__ == "__main__":
    main()