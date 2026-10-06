from typing import Any, Dict, List


class AuditAnalyzer:
    """
    Анализирует структурированный результат QA-аудита
    и выделяет только подтверждённые технические проблемы.

    Потенциально спорные случаи, зависящие от требований
    или бизнес-логики, в confirmed issues не добавляются.
    """

    def analyze(self, audit_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        issues = []

        issues.extend(self._analyze_http(audit_result))
        issues.extend(self._analyze_links(audit_result))
        issues.extend(self._analyze_ui_errors(audit_result))

        return issues

    def _analyze_http(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        issues = []

        http_result = audit_result.get("http", {})

        available = http_result.get("available")
        status_code = http_result.get("status_code")
        performance = http_result.get("performance")
        response_time = http_result.get("response_time")

        if available is False:
            issues.append(
                {
                    "category": "HTTP",
                    "title": "Сайт недоступен",
                    "description": (
                        "HTTP-проверка показала, что сайт недоступен."
                    ),
                    "evidence": {
                        "status_code": status_code,
                        "response_time": response_time,
                    },
                }
            )

        if (
            status_code is not None
            and status_code >= 400
        ):
            issues.append(
                {
                    "category": "HTTP",
                    "title": (
                        f"Главная страница возвращает HTTP "
                        f"{status_code}"
                    ),
                    "description": (
                        "Главная страница сайта возвращает "
                        "ошибочный HTTP status code."
                    ),
                    "evidence": {
                        "status_code": status_code,
                    },
                }
            )

        if performance == "WARN":
            issues.append(
                {
                    "category": "Performance",
                    "title": "Повышенное время HTTP-ответа",
                    "description": (
                        "Время ответа превышает порог PASS "
                        "и классифицировано как WARN."
                    ),
                    "evidence": {
                        "response_time": response_time,
                        "performance": performance,
                    },
                }
            )

        if performance == "FAIL":
            issues.append(
                {
                    "category": "Performance",
                    "title": "Высокое время HTTP-ответа",
                    "description": (
                        "Время HTTP-ответа превышает допустимый "
                        "порог и классифицировано как FAIL."
                    ),
                    "evidence": {
                        "response_time": response_time,
                        "performance": performance,
                    },
                }
            )

        return issues

    def _analyze_links(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        issues = []

        links_result = audit_result.get("links", {})
        broken_links = links_result.get("broken_links", [])

        if broken_links:
            issues.append(
                {
                    "category": "Links",
                    "title": "Обнаружены битые внутренние ссылки",
                    "description": (
                        f"Во время аудита найдено битых ссылок: "
                        f"{len(broken_links)}."
                    ),
                    "evidence": {
                        "broken_links_count": len(broken_links),
                        "broken_links": broken_links,
                    },
                }
            )

        return issues

    def _analyze_ui_errors(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        issues = []

        ui_result = audit_result.get("ui", {})

        ui_status = ui_result.get("status")
        error = ui_result.get("error")

        if ui_status == "ERROR":
            issues.append(
                {
                    "category": "UI",
                    "title": "Ошибка Selenium UI-аудита",
                    "description": (
                        "Selenium не смог корректно завершить "
                        "UI-проверку."
                    ),
                    "evidence": {
                        "error": error,
                        "status": ui_status,
                    },
                }
            )

        return issues