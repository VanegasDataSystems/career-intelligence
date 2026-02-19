from __future__ import annotations

import rio

from .. import data_models


class SearchJobCard(rio.Component):
    """Card displaying a search result job with title, company, and description."""

    job: data_models.SearchJobResult

    def build(self) -> rio.Component:
        children: list[rio.Component] = [
            rio.Text(self.job.title, style="heading3"),
            rio.Text(self.job.company or "Unknown company", style="heading2"),
        ]

        if self.job.description:
            children.append(rio.Separator())
            children.append(
                rio.Text(
                    self.job.description,
                    style=rio.TextStyle(italic=True),
                )
            )

        return rio.Card(
            rio.Column(
                *children,
                spacing=0.5,
                margin=1,
            ),
            margin_bottom=0.5,
        )
