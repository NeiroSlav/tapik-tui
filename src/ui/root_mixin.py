from textual.app import App

from actions.root import RootActions
from store import RootStore


class RootProviderMixin:
    """Миксин виджетов, помогающий получать доступ к store и actions приложения"""

    app: App[None]

    @property
    def root_store(self) -> RootStore:
        if not self.app or not hasattr(self.app, "root_store"):
            raise RuntimeError(
                "Root store is not available: widget not mounted inside TapikApp"
            )
        return self.app.root_store  # type: ignore

    @property
    def root_actions(self) -> RootActions:
        if not self.app or not hasattr(self.app, "root_actions"):
            raise RuntimeError(
                "Root actions are not available: widget not mounted inside TapikApp"
            )
        return self.app.root_actions  # type: ignore
