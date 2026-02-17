from __future__ import annotations

from typing import Callable

import rio


class SearchBar(rio.Component):
    """Search bar with text input and search button."""

    query: str = ""
    on_search: Callable[[str], None] = lambda _: None

    def _on_submit(self, event: rio.TextInputConfirmEvent) -> None:
        self.on_search(self.query)

    def _on_click(self) -> None:
        self.on_search(self.query)

    def build(self) -> rio.Component:
        return rio.Row(
            rio.TextInput(
                text=self.bind().query,
                label="Search roles...",
                on_confirm=self._on_submit,
                grow_x=True,
            ),
            rio.Button(
                "Search",
                on_press=self._on_click,
            ),
            spacing=1,
            align_y=0,
        )
