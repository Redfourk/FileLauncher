import socket
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Footer
from textual_fspicker import FileOpen
from textual import work


# 1. Define your focusable box once
class FocusBox(Static):
    can_focus = True


# 2. Put the logic in the Main App class
class FileLauncherUtility(App):
    CSS_PATH = "layout.tcss"
    BINDINGS = [("s", "open_picker", "Select File")]

    def compose(self) -> ComposeResult:
        yield Header()
        # Box 1: Title
        yield Static("FileLauncher", classes="title")
        # Box 2: The Status Box (Focusable)
        yield FocusBox("No file selected", classes="box", id="file-status")
        # Boxes 3-6: Other grid items
        yield FocusBox("Three", classes="box")
        yield FocusBox("Four", classes="box")
        yield FocusBox("Five", classes="box")
        yield FocusBox("Six", classes="box")
        yield Footer()

    def action_open_picker(self) -> None:
        """Triggers when you press 'S'"""

        def handle_file_selection(path: Path | None):
            if path:
                # Update UI and start the background worker
                self.query_one("#file-status", Static).update(f"Sending: {path.name}...")
                self.send_file(path)

        self.push_screen(FileOpen("."), callback=handle_file_selection)

    @work(thread=True)
    def send_file(self, path: Path):
        """This runs in a background thread so the UI stays smooth"""
        try:
            # IMPORTANT: Replace with the actual IP of the receiver
            RECEIVER_IP = "192.168.1.XX"
            PORT = 5001

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(5)  # Don't hang forever if IP is wrong
            client.connect((RECEIVER_IP, PORT))

            with open(path, "rb") as f:
                while chunk := f.read(4096):
                    client.sendall(chunk)

            client.close()
            # Success update
            self.call_from_thread(
                self.query_one("#file-status", Static).update,
                f"✅ [bold green]Sent:[/]\n{path.name}"
            )
        except Exception as e:
            self.call_from_thread(self.notify, f"Transfer Failed: {e}", severity="error")


if __name__ == "__main__":
    app = FileLauncherUtility()
    app.run()

