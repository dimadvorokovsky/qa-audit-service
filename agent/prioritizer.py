from typing import Any, Dict, List


class IssuePrioritizer:
    """
    Назначает приоритет найденным проблемам.
    """

    PRIORITY_ORDER = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    def prioritize(
        self,
        issues: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        prioritized_issues = []

        for issue in issues:
            issue_with_priority = issue.copy()
            issue_with_priority["priority"] = self._get_priority(issue)
            prioritized_issues.append(issue_with_priority)

        return sorted(
            prioritized_issues,
            key=lambda item: self.PRIORITY_ORDER.get(
                item["priority"],
                0,
            ),
            reverse=True,
        )

    def _get_priority(self, issue: Dict[str, Any]) -> str:
        category = issue.get("category")
        title = issue.get("title", "")
        evidence = issue.get("evidence", {})

        if title == "Сайт недоступен":
            return "CRITICAL"

        if (
            category == "HTTP"
            and evidence.get("status_code") is not None
            and evidence.get("status_code") >= 500
        ):
            return "CRITICAL"

        if title == "Обнаружены битые внутренние ссылки":
            broken_links_count = evidence.get(
                "broken_links_count",
                0,
            )

            if broken_links_count >= 10:
                return "HIGH"

            if broken_links_count >= 1:
                return "MEDIUM"

        if title == "Ошибка Selenium UI-аудита":
            return "HIGH"

        if title == "Высокое время HTTP-ответа":
            return "HIGH"

        if title == "Повышенное время HTTP-ответа":
            return "MEDIUM"

        if title == "Отсутствует Title":
            return "MEDIUM"

        if title == "Отсутствует H1":
            return "MEDIUM"

        if title == "Форма без обязательных полей":
            return "LOW"

        if title == "Изображения без alt":
            return "LOW"

        return "LOW"