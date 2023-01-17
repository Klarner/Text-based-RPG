from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, TextLog, Label, Static

class WorldUI(Static):
    def compose(self) -> ComposeResult:
        yield Label("World", id="WorldTitle")
        yield TextLog(max_lines=100, id="World", markup=True)

class InventoryUI(Static):
    def compose(self) -> ComposeResult:
        yield Label("Inventory", id="InventoryTitle")
        yield TextLog(max_lines=100, id="Inventory", markup=True)

class DisplayUI(Static):
    def compose(self) -> ComposeResult:
        yield WorldUI()
        yield InventoryUI()

class InteractionUI(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="What would you like to do?", id="Interaction")
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        event.input.value = ""

class TextRPG(App):
    TITLE = "Text-based RPG"
    CSS_PATH = "style.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Container(DisplayUI(), InteractionUI())
    
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

app = TextRPG()

if __name__ == "__main__":
    app.run()
