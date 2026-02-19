from __future__ import annotations

from typing import Callable

import rio


class SearchBar(rio.Component):
    """Search bar with text input and search button."""

    query: str = ""
    on_search: Callable[[str], None] = lambda _: None

    _current_text: str = ""

    def _on_change(self, event: rio.TextInputChangeEvent) -> None:
        self._current_text = event.text

    def _on_submit(self, event: rio.TextInputConfirmEvent) -> None:
        self._current_text = event.text
        self.on_search(event.text)

    def _on_click(self) -> None:
        self.on_search(self._current_text)

    def build(self) -> rio.Component:
        return rio.Row(
            rio.TextInput(
                text=self.bind().query,
                label="Search roles...",
                on_confirm=self._on_submit,
                on_change=self._on_change,
                grow_x=True,
            ),
            rio.Button(
                "Search",
                on_press=self._on_click,
            ),
            spacing=1,
            align_y=0,
        )
