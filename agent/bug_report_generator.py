from typing import Any, Dict, List


class BugReportGenerator:
    """
    Генерирует черновики bug reports
    на основе подтверждённых проблем.
    """

    def generate(
        self,
        issues: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        bug_reports = []

        for number, issue in enumerate(issues, start=1):
            bug_reports.append(
                self._build_bug_report(
                    issue=issue,
                    number=number,
                )
            )

        return bug_reports

    def _build_bug_report(
        self,
        issue: Dict[str, Any],
        number: int,
    ) -> Dict[str, Any]:
        title = issue.get("title", "Неизвестная проблема")
        category = issue.get("category", "General")
        priority = issue.get("priority", "LOW")
        description = issue.get("description", "")
        evidence = issue.get("evidence", {})

        return {
            "id": f"BUG-{number:03d}",
            "title": title,
            "category": category,
            "priority": priority,
            "preconditions": self._build_preconditions(issue),
            "steps": self._build_steps(issue),
            "expected_result": self._build_expected_result(issue),
            "actual_result": self._build_actual_result(
                issue=issue,
                description=description,
                evidence=evidence,
            ),
            "evidence": evidence,
        }

    def _build_preconditions(
        self,
        issue: Dict[str, Any],
    ) -> List[str]:
        category = issue.get("category")

        if category == "Links":
            return [
                "Проверяемый сайт доступен.",
                "Главная страница успешно загружена.",
            ]

        if category == "SEO/UI":
            return [
                "Проверяемая страница доступна.",
                "HTML страницы успешно загружен.",
            ]

        if category == "Accessibility":
            return [
                "Проверяемая страница доступна.",
                "На странице присутствуют изображения.",
            ]

        if category == "HTTP":
            return [
                "Есть сетевое подключение.",
                "Указан корректный URL проверяемого сайта.",
            ]

        if category == "Performance":
            return [
                "Есть стабильное сетевое подключение.",
                "Указан корректный URL проверяемого сайта.",
            ]

        if category == "UI":
            return [
                "Firefox и WebDriver доступны.",
                "Указан корректный URL проверяемого сайта.",
            ]

        return [
            "Указан корректный URL проверяемого сайта.",
        ]

    def _build_steps(
        self,
        issue: Dict[str, Any],
    ) -> List[str]:
        category = issue.get("category")
        title = issue.get("title", "")

        if title == "Обнаружены битые внутренние ссылки":
            return [
                "Открыть проверяемый сайт.",
                "Получить внутренние ссылки страницы.",
                "Последовательно выполнить HTTP-проверку ссылок.",
                "Зафиксировать ссылки с ошибочными HTTP status codes.",
            ]

        if title == "Отсутствует H1":
            return [
                "Открыть проверяемую страницу.",
                "Проанализировать DOM страницы.",
                "Найти элемент <h1>.",
            ]

        if title == "Отсутствует Title":
            return [
                "Открыть проверяемую страницу.",
                "Проанализировать HTML страницы.",
                "Проверить наличие элемента <title>.",
            ]

        if title == "Изображения без alt":
            return [
                "Открыть проверяемую страницу.",
                "Получить все элементы <img>.",
                "Проверить наличие атрибута alt.",
            ]

        if category == "HTTP":
            return [
                "Отправить HTTP-запрос на проверяемый URL.",
                "Зафиксировать полученный status code.",
            ]

        if category == "Performance":
            return [
                "Отправить HTTP-запрос на проверяемый URL.",
                "Измерить время HTTP-ответа.",
                "Сравнить результат с установленными порогами.",
            ]

        if category == "UI":
            return [
                "Запустить Selenium UI-проверку.",
                "Открыть проверяемый URL.",
                "Зафиксировать результат выполнения UI-аудита.",
            ]

        return [
            "Открыть проверяемую страницу.",
            "Выполнить соответствующую проверку.",
            "Зафиксировать фактический результат.",
        ]

    def _build_expected_result(
        self,
        issue: Dict[str, Any],
    ) -> str:
        title = issue.get("title", "")

        if title == "Обнаружены битые внутренние ссылки":
            return (
                "Внутренние ссылки должны вести на доступные страницы "
                "и не возвращать ошибочные HTTP status codes."
            )

        if title == "Отсутствует H1":
            return (
                "На странице должен присутствовать H1, "
                "если это предусмотрено требованиями страницы."
            )

        if title == "Отсутствует Title":
            return (
                "В HTML страницы должен присутствовать "
                "непустой элемент <title>."
            )

        if title == "Изображения без alt":
            return (
                "Изображения должны содержать корректный атрибут alt "
                "с учётом требований доступности и назначения изображения."
            )

        if title == "Сайт недоступен":
            return (
                "Сайт должен быть доступен и успешно отвечать "
                "на HTTP-запрос."
            )

        if title.startswith("Главная страница возвращает HTTP"):
            return (
                "Главная страница должна возвращать успешный "
                "HTTP status code."
            )

        if title in (
            "Повышенное время HTTP-ответа",
            "Высокое время HTTP-ответа",
        ):
            return (
                "Время HTTP-ответа должно соответствовать "
                "установленному порогу производительности."
            )

        if title == "Ошибка Selenium UI-аудита":
            return (
                "Selenium UI-аудит должен завершаться "
                "без технических ошибок."
            )

        return "Фактический результат должен соответствовать требованиям."

    def _build_actual_result(
        self,
        issue: Dict[str, Any],
        description: str,
        evidence: Dict[str, Any],
    ) -> str:
        title = issue.get("title", "")

        if title == "Обнаружены битые внутренние ссылки":
            count = evidence.get("broken_links_count", 0)

            return (
                f"Обнаружено битых внутренних ссылок: {count}."
            )

        if title == "Отсутствует H1":
            return "На странице не обнаружен элемент <h1>."

        if title == "Отсутствует Title":
            return "На странице не обнаружен элемент <title>."

        if title == "Изображения без alt":
            count = evidence.get("images_without_alt", 0)

            return (
                f"Обнаружено изображений без alt: {count}."
            )

        if title == "Сайт недоступен":
            return (
                "HTTP-проверка показала, что сайт недоступен."
            )

        if title.startswith("Главная страница возвращает HTTP"):
            status_code = evidence.get("status_code")

            return (
                f"Получен HTTP status code: {status_code}."
            )

        if title in (
            "Повышенное время HTTP-ответа",
            "Высокое время HTTP-ответа",
        ):
            response_time = evidence.get("response_time")

            return (
                f"Зафиксировано время HTTP-ответа: "
                f"{response_time} сек."
            )

        if title == "Ошибка Selenium UI-аудита":
            error = evidence.get("error")

            return (
                f"Selenium UI-аудит завершился ошибкой: {error}."
            )

        return description