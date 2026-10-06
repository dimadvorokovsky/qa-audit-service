from typing import Any, Dict, List


class QASummaryGenerator:
    """
    Формирует краткое QA-заключение
    на основе подтверждённых проблем и manual checks.
    """

    def generate(
        self,
        issues: List[Dict[str, Any]],
        manual_checks: List[Dict[str, Any]],
    ) -> str:
        total_issues = len(issues)

        critical_count = self._count_priority(issues, "CRITICAL")
        high_count = self._count_priority(issues, "HIGH")
        medium_count = self._count_priority(issues, "MEDIUM")
        low_count = self._count_priority(issues, "LOW")

        summary_lines = [
            "QA SUMMARY",
            "",
            f"Подтверждённых проблем: {total_issues}",
            f"CRITICAL: {critical_count}",
            f"HIGH: {high_count}",
            f"MEDIUM: {medium_count}",
            f"LOW: {low_count}",
            f"Требуют ручной проверки: {len(manual_checks)}",
            "",
        ]

        summary_lines.extend(
            self._build_overall_conclusion(
                critical_count=critical_count,
                high_count=high_count,
                medium_count=medium_count,
                low_count=low_count,
            )
        )

        if issues:
            summary_lines.append("")
            summary_lines.append("Основные проблемы:")

            for issue in issues:
                summary_lines.append(
                    f"- [{issue['priority']}] "
                    f"{issue['title']}"
                )

        if manual_checks:
            summary_lines.append("")
            summary_lines.append("Что проверить вручную:")

            for check in manual_checks:
                summary_lines.append(
                    f"- {check['title']}"
                )

        return "\n".join(summary_lines)

    def _count_priority(
        self,
        issues: List[Dict[str, Any]],
        priority: str,
    ) -> int:
        return sum(
            1
            for issue in issues
            if issue.get("priority") == priority
        )

    def _build_overall_conclusion(
        self,
        critical_count: int,
        high_count: int,
        medium_count: int,
        low_count: int,
    ) -> List[str]:
        if critical_count > 0:
            return [
                "Итог: обнаружены критические проблемы.",
                (
                    "Рекомендуется устранить CRITICAL-дефекты "
                    "до дальнейшего релиза или использования."
                ),
            ]

        if high_count > 0:
            return [
                "Итог: обнаружены серьёзные проблемы.",
                (
                    "Рекомендуется в первую очередь устранить "
                    "HIGH-дефекты и затем выполнить повторный аудит."
                ),
            ]

        if medium_count > 0:
            return [
                "Итог: обнаружены проблемы среднего приоритета.",
                (
                    "Сайт доступен, но найденные проблемы "
                    "желательно исправить и перепроверить."
                ),
            ]

        if low_count > 0:
            return [
                "Итог: критических проблем не обнаружено.",
                (
                    "Есть замечания низкого приоритета, "
                    "которые рекомендуется исправить."
                ),
            ]

        return [
            "Итог: подтверждённых проблем не обнаружено.",
            (
                "Рекомендуется выполнить manual checks "
                "для проверки спорных сценариев."
            ),
        ]