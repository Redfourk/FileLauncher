import os, sys
from pathlib import Path

# Adds the 'src' directory to the path so layout.py can find other modules
sys.path.append(str(Path(__file__).parent.parent))

import socket
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Header, Footer
from textual_fspicker import FileOpen
from textual import work


# 1. Define a focusable box for your grid
class FocusBox(Static):
    can_focus = True


# 2. The main Application logic
class FileLauncherUtility(App):
    CSS_PATH = "layout.tcss"
    BINDINGS = [
        ("s", "open_picker", "Select File"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("FileLauncher\nVersion: 0.1.0-test.1", classes="title")

        # Box 2: The Status Box (Focusable)
        yield FocusBox("No file selected", classes="box", id="file-status")

        # Boxes 3-6: Other grid items
        yield FocusBox("Three", classes="box")
        yield FocusBox("Instructions:\nPress 'S' to select", classes="box")
        yield FocusBox("Five", classes="box")
        yield FocusBox("Six", classes="box")

        yield Footer()


    def action_open_picker(self) -> None:
        # 1. Folder path (Ensure this is a folder, not a file!)
        target_folder = r"C:\Users\082096\Downloads"

        # 2. What happens after selection
        def handle_file_selection(path: Path | None) -> None:
            if path and path.is_file():
                self.query_one("#file-status", Static).update(f"Sending: {path.name}...")
                self.send_file(path)
            elif path:
                self.notify("You selected a folder. Please pick a file!")

        # 3. Setup and Push Picker (Moved outside the function above)
        picker = FileOpen(target_folder)
        self.push_screen(picker, callback=handle_file_selection)

        # 4. Focus logic
        def grab_file_list():
            try:
                tree = picker.query_one("DirectoryTree")
                tree.focus()
            except:
                pass

        # Call the timer using the correct function name
        self.set_timer(0.1, grab_file_list)

    @work(thread=True)
    def send_file(self, path: Path):
        try:
            RECEIVER_IP = "127.0.0.1"  # Change this for real transfers!
            PORT = 5001

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)
            client.connect((RECEIVER_IP, PORT))

            with open(path, "rb") as f:
                while chunk := f.read(4096):
                    client.sendall(chunk)

            client.close()

            self.call_from_thread(
                self.query_one("#file-status", Static).update,
                f"✅ [bold green]Sent:[/]\n{path.name}"
            )
        except Exception as e:
            self.call_from_thread(self.notify, f"Transfer Error: {e}", severity="error")
            self.call_from_thread(
                self.query_one("#file-status", Static).update,
                "[red]Transfer Failed[/]\nPress 'S' to retry"
            )

    def on_key(self, event) -> None:
        """Forces the 'S' key to work regardless of which box is focused."""
        if event.key.lower() == "s":
            self.action_open_picker()


    def on_mount(self):
        self.title = "FileLauncher CLI"


if __name__ == "__main__":
    app = FileLauncherUtility()
    app.run()

