from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Welcome

title_content = """
FileLauncher

Version: 0.1.0-test.1
"""
bottom_left_content = """
Instructions:

1. Press 'S' to select 
the file you want to 
transfer.
2. Code that in
3. Actually make the 
app....-_-
"""
class GridLayout(App):
    CSS_PATH = "layout.tcss"

    def compose(self) -> ComposeResult:
        yield Static(title_content, classes="title")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")
        yield Static(bottom_left_content, classes="box")
        yield Static("Five", classes="box")
        yield Static("Six", classes="box")


if __name__ == "__main__":
    app = GridLayout()
    app.run()