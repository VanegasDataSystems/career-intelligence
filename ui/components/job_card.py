from __future__ import annotations

import rio

from .. import data_models


class SearchJobCard(rio.Component):
    """Card displaying a search result job with score and skills."""

    job: data_models.SearchJobResult

    def build(self) -> rio.Component:
        children: list[rio.Component] = [
            rio.Row(
                rio.Text(self.job.title, style="heading3", grow_x=True),
                rio.Text(
                    f"Score: {self.job.score:.2f}",
                    style=rio.TextStyle(
                        font_size=0.85,
                        fill=rio.Color.from_hex("0083ff"),
                        font_weight="bold",
                    ),
                ),
                spacing=1,
            ),
            rio.Text(self.job.company or "Unknown company", style="heading2"),
        ]

        if self.job.location:
            children.append(
                rio.Text(
                    self.job.location,
                    style=rio.TextStyle(italic=True),
                )
            )

        if self.job.skills:
            skills_text = ", ".join(self.job.skills[:6])
            if len(self.job.skills) > 6:
                skills_text += f" +{len(self.job.skills) - 6} more"
            children.append(
                rio.Text(
                    f"Skills: {skills_text}",
                    style=rio.TextStyle(
                        font_size=0.8,
                        fill=rio.Color.from_hex("666666"),
                    ),
                )
            )

        children.append(
            rio.Link(
                rio.Text("Apply"),
                target_url=self.job.url,
                open_in_new_tab=True,
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


class JobCard(rio.Component):
    """A card component displaying a job listing."""

    job: data_models.JobListing

    def build(self) -> rio.Component:
        # Format salary range if available
        salary_text = ""
        if self.job.salary_min and self.job.salary_max:
            salary_text = f"${self.job.salary_min:,} - ${self.job.salary_max:,}"
        elif self.job.salary_min:
            salary_text = f"From ${self.job.salary_min:,}"
        elif self.job.salary_max:
            salary_text = f"Up to ${self.job.salary_max:,}"

        children: list[rio.Component] = [
            rio.Text(
                self.job.position,
                style="heading3",
            ),
            rio.Text(
                self.job.company,
                style="heading2",
            ),
        ]

        if self.job.location:
            children.append(
                rio.Text(
                    self.job.location,
                    style=rio.TextStyle(italic=True),
                )
            )

        if salary_text:
            children.append(
                rio.Text(
                    salary_text,
                    style=rio.TextStyle(fill=rio.Color.from_hex("2e7d32")),
                )
            )

        if self.job.tags:
            children.append(
                rio.Text(
                    self.job.tags,
                    style=rio.TextStyle(
                        font_size=0.8,
                        fill=rio.Color.from_hex("666666"),
                    ),
                )
            )

        children.append(
            rio.Link(
                rio.Text("Apply"),
                target_url=self.job.url,
                open_in_new_tab=True,
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
