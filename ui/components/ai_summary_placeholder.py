from __future__ import annotations

import rio


class AiSummaryPlaceholder(rio.Component):
    """Card showing an AI summary or placeholder text."""

    summary_text: str = "Text summary goes here..."

    def build(self) -> rio.Component:
        return rio.Card(
            rio.Column(
                rio.Text(
                    self.summary_text,
                    style=rio.TextStyle(italic=True, fill=rio.Color.from_hex("777777")),
                ),
                spacing=0.5,
                margin=1,
            ),
        )
