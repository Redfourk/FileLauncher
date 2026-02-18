def main():
    import os
    import subprocess
    import sys
    from pathlib import Path
    import tkinter as tk
    from tkinter import ttk
    from tkinter.font import names

    original_dir = os.getcwd()

    def graphical_button_operation():
        print("Graphical button pressed!")

    def command_line_button_operation():
        print("Command line button pressed!")
        script_dir = Path(__file__).parent.resolve()
        target_script = script_dir / "command_line" / "layout.py"
        print(f"Attempting to launch: {target_script}")
        try:
            subprocess.Popen(
                [sys.executable, str(target_script)],
                creationflags=0x00000010
            )
            print("Launch command sent successfully.")
            prompt.after(100, close_app)
        except Exception as e:
            print(f"FAILED to launch: {e}")

    prompt = tk.Tk()
    prompt.style = ttk.Style()
    prompt.style.theme_use('classic')

    prompt.title("Info")

    prompt.update_idletasks()
    width = 350
    height = 150
    screen_width = prompt.winfo_screenwidth()
    screen_height = prompt.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    prompt.geometry(f"{width}x{height}+{x}+{y}")



    prompt.configure(bg="#c0c0c0")
    prompt.overrideredirect(True)

    TITLE_BLUE = "#000080"
    TEXT_WHITE = "#ffffff"
    WIN95_GRAY = "#c0c0c0"

    title_bar = tk.Frame(prompt, bg=TITLE_BLUE, height=20, relief="raised", bd=0)
    title_bar.pack(expand=False, fill="x")

    title_label = tk.Label(title_bar, text=" FileLauncher",
                           bg=TITLE_BLUE, fg=TEXT_WHITE,
                           font=("MS Sans Serif", 8, "bold"))
    title_label.pack(side="left")

    def close_app():
        prompt.destroy()

    close_btn = tk.Button(title_bar, text="r", font=("Marlett", 10),  # 'r' is 'X' in Marlett font
                          width=2, height=1, bg=WIN95_GRAY, relief="raised",
                          borderwidth=1, command=close_app)
    close_btn.pack(side="right", padx=2, pady=2)

    def start_move(event):
        prompt.x = event.x
        prompt.y = event.y

    def stop_move(event):
        prompt.x = None
        prompt.y = None

    def moving(event):
        x = (event.x_root - prompt.x)
        y = (event.y_root - prompt.y)
        prompt.geometry(f"+{x}+{y}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)
    title_bar.bind("<B1-Motion>", moving)

    WIN95_GRAY = "#c0c0c0"
    WIN95_FONT = ("MS Sans Serif", 8)

    question = tk.Label(prompt,
                        text="\nFileLauncher has Graphical User Interface capabilities.\n Would you like to use the GUI, \nor stay in a command line interface?",
                        bg="#c0c0c0").pack()

    btn_options_graphical = {
        "bg": WIN95_GRAY,
        "font": WIN95_FONT,
        "relief": "raised",
        "borderwidth": 2,
        "activebackground": "#d9d9d9",  # Slightly lighter gray when clicked
        "command": graphical_button_operation,
    }

    btn_options_command_line = {
        "bg": WIN95_GRAY,
        "font": WIN95_FONT,
        "relief": "raised",
        "borderwidth": 2,
        "activebackground": "#d9d9d9",  # Slightly lighter gray when clicked
        "command": command_line_button_operation,
    }

    graphical_option = tk.Button(prompt, text="GUI", width=10, **btn_options_graphical)
    graphical_option.pack(side="left", padx=10, pady=10)

    command_line_option = tk.Button(prompt, text="COMMAND LINE", width=15, **btn_options_command_line)
    command_line_option.pack(side="right", padx=10, pady=10)

    prompt.mainloop()

if __name__ == "__main__":
    main()
