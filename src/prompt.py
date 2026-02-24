import ctypes

def main():
    import os
    import subprocess
    import sys
    from pathlib import Path

    if sys.platform.startswith("win"):
        myappid = 'Redfourk.FileLauncher.0.1.0.prompt'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    import tkinter as tk
    from tkinter import ttk
    base_dir = Path(__file__).parent.resolve()
    icon_path = base_dir / "assets" / "FileLauncher16.ico"
    def graphical_button_operation():
        target_script = base_dir / "gui" / "gui.pyw"
        python_exe = sys.executable.lower().replace("python.exe", "pythonw.exe")
        try:
            subprocess.Popen(
                [python_exe, str(target_script)],
                creationflags=0x00000008,
                close_fds=True,
                start_new_session=True,
                cwd=str(base_dir)
            )
            prompt.after(100, close_app)
        except Exception:
            subprocess.Popen([sys.executable, str(target_script)])
    def command_line_button_operation():
        base_dir = Path(__file__).parent.resolve()
        target_script = base_dir / "command_line" / "layout.py"
        cmd_str = f'cmd /c start "" "{sys.executable}" "{target_script}"'

        try:
            subprocess.Popen(
                cmd_str,
                shell=True,
                cwd=str(base_dir),
                creationflags=0x00000010,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True
            )
            prompt.after(200, close_app)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Launch Error", f"Critical Failure:\n{e}")
    prompt = tk.Tk()
    if icon_path.exists():
        prompt.iconbitmap(str(icon_path))
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
    def show_in_taskbar(window):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = (style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        window.withdraw()
        window.after(10, window.deiconify)
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
    tk.Button(prompt, text="GUI", width=10, command=graphical_button_operation, **btn_opts).pack(side="left", padx=10,
                                                                                         pady=10)
    tk.Button(prompt, text="COMMAND LINE", width=15, command=command_line_button_operation, **btn_opts).pack(
        side="right", padx=10, pady=10)


    prompt.mainloop()


if __name__ == "__main__":
    main()
