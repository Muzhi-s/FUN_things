from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from core.meeting import MeetingResult


@dataclass
class ReportWriter:
    reports_dir: Path = Path(__file__).resolve().parents[1] / "reports"

    def build_content(self, result: MeetingResult) -> str:
        sections = [
            "# Meeting Report",
            "## Question",
            result.question,
            "## Planner",
            self._get_response(result, "Planner"),
            "## Executor",
            self._get_response(result, "Executor"),
            "## Challenger",
            self._get_response(result, "Challenger"),
            "## Coordinator",
            self._get_response(result, "Coordinator"),
        ]
        return "\n\n".join(sections).strip() + "\n"

    def save(self, result: MeetingResult) -> Path:
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = self._next_report_path()
        report_path.write_text(self.build_content(result), encoding="utf-8")
        return report_path

    def _next_report_path(self) -> Path:
        today = date.today().isoformat()
        index = 1

        while True:
            candidate = self.reports_dir / f"{today}-{index:03d}.md"
            if not candidate.exists():
                return candidate
            index += 1

    @staticmethod
    def _get_response(result: MeetingResult, role: str) -> str:
        for response in result.analyses:
            if response.role == role:
                return response.content.strip()
        if result.final_summary.role == role:
            return result.final_summary.content.strip()
        return ""


def save_report(result: MeetingResult, reports_dir: str | Path | None = None) -> Path:
    writer = ReportWriter(Path(reports_dir) if reports_dir is not None else ReportWriter.reports_dir)
    return writer.save(result)
