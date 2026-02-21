from __future__ import annotations

import rio


@rio.page(
    name="About",
    url_segment="about",
)
class AboutPage(rio.Component):
    """Simple about page."""

    def build(self) -> rio.Component:
        return rio.Column(
            rio.Text("About", style="heading1"),
            rio.Text("Career Intelligence - Job listings aggregator."),
            margin=2,
            spacing=1,
        )
