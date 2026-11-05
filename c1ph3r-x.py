from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DirectoryTree

class Sidebar(Static):
    def compose(self) -> ComposeResult:
        yield DirectoryTree("./")

class Editor(Static):
    def compose(self) -> ComposeResult:
        yield Static("Welcome to C1PH3R-X [VERSION 0.1]")

class C1PH3R(App):
    """The most powerful terminal IDE ever created."""
    
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Toggle Dark Mode")]
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 20 1fr;
    }
    Sidebar { background: #1a1a1a; height: 100%; border-right: vkey #333; }
    Editor { background: #0d0d0d; height: 100%; padding: 2; }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar()
        yield Editor()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = C1PH3R()
    app.run()
