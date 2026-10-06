from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class AgentReportWriter:
    """
    Сохраняет результат работы QA Agent
    в отдельный Markdown-отчёт.

    Детерминированные результаты и LLM-анализ
    сохраняются в отдельных разделах.
    """

    def save(
        self,
        url: str,
        agent_result: Dict[str, Any],
        llm_result: Optional[Dict[str, Any]] = None,
        output_dir: str = "reports",
    ) -> str:
        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = Path(output_dir) / (
            f"agent_{timestamp}.md"
        )

        content = self._build_report(
            url=url,
            agent_result=agent_result,
            llm_result=llm_result,
        )

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return str(file_path)

    def _build_report(
        self,
        url: str,
        agent_result: Dict[str, Any],
        llm_result: Optional[Dict[str, Any]] = None,
    ) -> str:
        issues = agent_result.get(
            "issues",
            [],
        )

        manual_checks = agent_result.get(
            "manual_checks",
            [],
        )

        summary = agent_result.get(
            "summary",
            "",
        )

        bug_reports = agent_result.get(
            "bug_reports",
            [],
        )

        lines = [
            "# QA Agent Report",
            "",
            f"**URL:** {url}",
            "",
            (
                f"**Generated:** "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ),
            "",
            "---",
            "",
            "## Deterministic QA Summary",
            "",
            "```text",
            summary,
            "```",
            "",
            "---",
            "",
        ]

        lines.extend(
            self._build_confirmed_issues(
                issues
            )
        )

        lines.extend(
            self._build_manual_checks(
                manual_checks
            )
        )

        lines.extend(
            self._build_bug_reports(
                bug_reports
            )
        )

        lines.extend(
            self._build_llm_analysis(
                llm_result
            )
        )

        return "\n".join(lines)

    def _build_confirmed_issues(
        self,
        issues: List[Dict[str, Any]],
    ) -> List[str]:
        lines = [
            "## Confirmed Issues",
            "",
            f"Всего: **{len(issues)}**",
            "",
        ]

        if not issues:
            lines.extend(
                [
                    "Подтверждённых проблем не обнаружено.",
                    "",
                    "---",
                    "",
                ]
            )

            return lines

        for number, issue in enumerate(
            issues,
            start=1,
        ):
            lines.extend(
                [
                    (
                        f"### {number}. "
                        f"[{issue.get('priority', 'LOW')}] "
                        f"{issue.get('title', '')}"
                    ),
                    "",
                    (
                        f"**Category:** "
                        f"{issue.get('category', '')}"
                    ),
                    "",
                    (
                        f"**Description:** "
                        f"{issue.get('description', '')}"
                    ),
                    "",
                    "**Evidence:**",
                    "",
                    "```text",
                    self._format_value(
                        issue.get(
                            "evidence",
                            {},
                        )
                    ),
                    "```",
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                "",
            ]
        )

        return lines

    def _build_manual_checks(
        self,
        manual_checks: List[Dict[str, Any]],
    ) -> List[str]:
        lines = [
            "## Manual Checks",
            "",
            (
                f"Требуют ручной проверки: "
                f"**{len(manual_checks)}**"
            ),
            "",
        ]

        if not manual_checks:
            lines.extend(
                [
                    (
                        "Дополнительные manual checks "
                        "не сформированы."
                    ),
                    "",
                    "---",
                    "",
                ]
            )

            return lines

        for number, check in enumerate(
            manual_checks,
            start=1,
        ):
            lines.extend(
                [
                    (
                        f"### {number}. "
                        f"{check.get('title', '')}"
                    ),
                    "",
                    (
                        f"**Category:** "
                        f"{check.get('category', '')}"
                    ),
                    "",
                    (
                        f"**Reason:** "
                        f"{check.get('reason', '')}"
                    ),
                    "",
                    "**Context:**",
                    "",
                    "```text",
                    self._format_value(
                        check.get(
                            "context",
                            {},
                        )
                    ),
                    "```",
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                "",
            ]
        )

        return lines

    def _build_bug_reports(
        self,
        bug_reports: List[Dict[str, Any]],
    ) -> List[str]:
        lines = [
            "## Bug Report Drafts",
            "",
            (
                f"Создано черновиков: "
                f"**{len(bug_reports)}**"
            ),
            "",
        ]

        if not bug_reports:
            lines.extend(
                [
                    "Черновики bug reports не сформированы.",
                    "",
                    "---",
                    "",
                ]
            )

            return lines

        for bug in bug_reports:
            lines.extend(
                [
                    (
                        f"### {bug.get('id', '')} — "
                        f"{bug.get('title', '')}"
                    ),
                    "",
                    (
                        f"**Category:** "
                        f"{bug.get('category', '')}"
                    ),
                    "",
                    (
                        f"**Priority:** "
                        f"{bug.get('priority', '')}"
                    ),
                    "",
                    "#### Preconditions",
                    "",
                ]
            )

            for item in bug.get(
                "preconditions",
                [],
            ):
                lines.append(
                    f"- {item}"
                )

            lines.extend(
                [
                    "",
                    "#### Steps",
                    "",
                ]
            )

            for number, step in enumerate(
                bug.get(
                    "steps",
                    [],
                ),
                start=1,
            ):
                lines.append(
                    f"{number}. {step}"
                )

            lines.extend(
                [
                    "",
                    "#### Expected Result",
                    "",
                    bug.get(
                        "expected_result",
                        "",
                    ),
                    "",
                    "#### Actual Result",
                    "",
                    bug.get(
                        "actual_result",
                        "",
                    ),
                    "",
                    "#### Evidence",
                    "",
                    "```text",
                    self._format_value(
                        bug.get(
                            "evidence",
                            {},
                        )
                    ),
                    "```",
                    "",
                    "---",
                    "",
                ]
            )

        return lines

    def _build_llm_analysis(
        self,
        llm_result: Optional[Dict[str, Any]],
    ) -> List[str]:
        lines = [
            "## LLM Analysis",
            "",
        ]

        if llm_result is None:
            lines.extend(
                [
                    "**Status:** not_run",
                    "",
                    (
                        "LLM-анализ не запускался для "
                        "этого отчёта."
                    ),
                    "",
                ]
            )

            return lines

        status_value = llm_result.get(
            "status",
            "unknown",
        )

        lines.extend(
            [
                f"**Status:** {status_value}",
                "",
            ]
        )

        if status_value != "success":
            lines.extend(
                [
                    (
                        f"**Reason:** "
                        f"{llm_result.get('reason', '')}"
                    ),
                    "",
                    (
                        "Детерминированные результаты "
                        "аудита остаются доступными выше."
                    ),
                    "",
                ]
            )

            return lines

        analysis = llm_result.get(
            "analysis",
            {},
        )

        lines.extend(
            [
                "### Executive Summary",
                "",
                analysis.get(
                    "executive_summary",
                    "",
                ),
                "",
                "### Risk Assessment",
                "",
                analysis.get(
                    "risk_assessment",
                    "",
                ),
                "",
                "### Additional Manual Checks",
                "",
            ]
        )

        additional_checks = analysis.get(
            "additional_manual_checks",
            [],
        )

        if not additional_checks:
            lines.append(
                "Дополнительных проверок не предложено."
            )
        else:
            for number, check in enumerate(
                additional_checks,
                start=1,
            ):
                lines.extend(
                    [
                        (
                            f"{number}. "
                            f"**{check.get('title', '')}**"
                        ),
                        (
                            f"   - Reason: "
                            f"{check.get('reason', '')}"
                        ),
                    ]
                )

        lines.extend(
            [
                "",
                "### Bug Report Improvements",
                "",
            ]
        )

        improvements = analysis.get(
            "bug_report_improvements",
            [],
        )

        if not improvements:
            lines.append(
                "Предложений по улучшению нет."
            )
        else:
            for number, improvement in enumerate(
                improvements,
                start=1,
            ):
                lines.extend(
                    [
                        (
                            f"{number}. "
                            f"**{improvement.get('issue', '')}**"
                        ),
                        (
                            f"   - Suggestion: "
                            f"{improvement.get('suggestion', '')}"
                        ),
                    ]
                )

        lines.extend(
            [
                "",
                "### Confidence Notes",
                "",
            ]
        )

        confidence_notes = analysis.get(
            "confidence_notes",
            [],
        )

        if not confidence_notes:
            lines.append(
                "Комментариев по уверенности нет."
            )
        else:
            for note in confidence_notes:
                lines.append(
                    f"- {note}"
                )

        lines.extend(
            [
                "",
                "---",
                "",
                (
                    "> LLM analysis is advisory. "
                    "Confirmed Issues above are produced "
                    "by deterministic checks and remain "
                    "the source of factual audit evidence."
                ),
                "",
            ]
        )

        return lines

    def _format_value(
        self,
        value: Any,
        indent: int = 0,
    ) -> str:
        """
        Форматирует вложенные структуры так,
        чтобы Evidence и Context были читаемыми.
        """

        prefix = " " * indent

        if isinstance(value, dict):
            lines = []

            for key, item in value.items():
                if isinstance(item, list):
                    lines.append(
                        f"{prefix}{key}:"
                    )

                    lines.extend(
                        self._format_list(
                            item,
                            indent=indent + 2,
                        )
                    )

                elif isinstance(item, dict):
                    lines.append(
                        f"{prefix}{key}:"
                    )

                    formatted = self._format_value(
                        item,
                        indent=indent + 2,
                    )

                    lines.extend(
                        formatted.splitlines()
                    )

                else:
                    lines.append(
                        f"{prefix}{key}: {item}"
                    )

            return "\n".join(lines)

        if isinstance(value, list):
            return "\n".join(
                self._format_list(
                    value,
                    indent=indent,
                )
            )

        return f"{prefix}{value}"

    def _format_list(
        self,
        items: List[Any],
        indent: int = 0,
    ) -> List[str]:
        lines = []
        prefix = " " * indent

        for item in items:
            if isinstance(item, dict):
                url = item.get("url")
                status_code = item.get(
                    "status_code"
                )

                if (
                    url is not None
                    and status_code is not None
                ):
                    lines.append(
                        f"{prefix}- "
                        f"{status_code} | {url}"
                    )

                else:
                    lines.append(
                        f"{prefix}-"
                    )

                    formatted = self._format_value(
                        item,
                        indent=indent + 2,
                    )

                    lines.extend(
                        formatted.splitlines()
                    )

            else:
                lines.append(
                    f"{prefix}- {item}"
                )

        return lines