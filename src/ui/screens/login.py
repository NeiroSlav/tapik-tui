from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Label

from handlers.handle_login import handle_login


class LoginScreen(Vertical):
    DEFAULT_CSS = """

    LoginScreen {
        align-horizontal: center;
        align-vertical: middle;
    }

    LoginScreen > Vertical {
        width: 30;
        height: auto;
        padding: 1 2;
        align-horizontal: center;
        align-vertical: middle;
        background: $surface 50%;
    }

    LoginScreen > Vertical > Label {
        width: 100%;
        content-align: center middle;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        self.login_input = Input(
            placeholder="login",
            id="login",
        )
        self.pass_input = Input(
            placeholder="password",
            password=True,
            id="password",
        )

        yield Vertical(
            Label("TAPIK MESSANGER"),
            self.login_input,
            self.pass_input,
        )

    async def on_input_submitted(self, event: Input.Submitted):
        """Enter в input'ах."""

        # Enter в поле логина - фокус на пароль
        if event.input.id == "login":
            self.pass_input.focus()
            return

        # Enter в поле пароля - вызвать внешний callback
        if event.input.id == "password":
            login = self.login_input.value
            password = self.pass_input.value
            await handle_login(login, password)
