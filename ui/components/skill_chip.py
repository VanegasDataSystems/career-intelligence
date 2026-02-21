from __future__ import annotations

import rio


class SkillChip(rio.Component):
    """Small chip showing a skill name and its relevance score."""

    name: str = ""
    score: float = 0.0

    def build(self) -> rio.Component:
        return rio.Card(
            rio.Row(
                rio.Text(
                    self.name,
                    style=rio.TextStyle(font_size=0.85, font_weight="bold"),
                ),
                rio.Text(
                    f"{self.score:.0%}",
                    style=rio.TextStyle(
                        font_size=0.8,
                        fill=rio.Color.from_hex("555555"),
                    ),
                ),
                spacing=0.4,
                margin_x=0.6,
                margin_y=0.3,
            ),
        )
