from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message as TMessageEvent
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Input


class MessageInputWidget(Widget):
    """Область ввода нового сообщения с кнопкой отправки."""

    # текущее содержимое input
    text = reactive("")

    DEFAULT_CSS = """
    MessageInputWidget {
        dock: bottom;
        width: 100%;
        height: auto;
    }

    MessageInputWidget Horizontal {
        width: 100%;
        height: auto;
    }

    Input {
        width: 80%;
        height: auto;
        min-height: 1;
        padding: 0 0;
    }

    Button {
        width: auto;
        margin-left: 1;
        background: red;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            self.input = Input(placeholder="Введите сообщение...")
            self.send_button = Button("Send", id="send-btn")
            yield self.input
            yield self.send_button

    async def on_input_changed(self, event: Input.Changed) -> None:
        """Обновляем reactive text при вводе."""
        self.text = event.value

    # async def on_button_pressed(self, event: Button.Pressed) -> None:
    #     """Обработка нажатия кнопки."""
    #     if event.button is self.send_button and self.text.strip():
    #         await self.emit(self.MessageSent(self.text))
    #         self.input.value = ""
    #         self.text = ""

    class MessageSent(TMessageEvent):
        """Событие: пользователь отправил сообщение."""

        def __init__(self, content: str) -> None:
            self.content = content
            super().__init__()
