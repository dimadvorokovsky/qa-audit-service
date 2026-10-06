from typing import Any, Dict, List


class ManualCheckGenerator:
    """
    Формирует список проверок, которые нельзя уверенно
    классифицировать как подтверждённые дефекты автоматически
    и которые требуют ручной проверки QA-инженером.
    """

    def generate(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        checks = []

        checks.extend(self._check_forms(audit_result))
        checks.extend(self._check_ui_context(audit_result))
        checks.extend(self._check_images(audit_result))

        return checks

    def _check_forms(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        checks = []

        forms_result = audit_result.get("forms", {})
        forms = forms_result.get("forms", [])

        for form in forms:
            fields = form.get("fields", [])

            if not fields:
                continue

            required_fields = [
                field
                for field in fields
                if field.get("required") is True
            ]

            if not required_fields:
                checks.append(
                    {
                        "category": "Forms",
                        "title": (
                            "Проверить необходимость обязательных "
                            "полей формы"
                        ),
                        "reason": (
                            "В форме не обнаружено полей с атрибутом "
                            "required. Это не обязательно является "
                            "дефектом и требует проверки бизнес-логики."
                        ),
                        "context": {
                            "method": form.get("method"),
                            "action": form.get("action"),
                            "instances": form.get("instances", 1),
                            "fields_count": len(fields),
                        },
                    }
                )

        return checks

    def _check_ui_context(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        checks = []

        ui_result = audit_result.get("ui", {})

        h1_exists = ui_result.get("h1_exists")
        title_exists = ui_result.get("title_exists")

        if h1_exists is False:
            checks.append(
                {
                    "category": "SEO/UI",
                    "title": (
                        "Проверить требования к H1 "
                        "на конкретном типе страницы"
                    ),
                    "reason": (
                        "H1 отсутствует. Автоматическая проверка "
                        "фиксирует факт, но необходимость H1 зависит "
                        "от требований и структуры страницы."
                    ),
                    "context": {
                        "h1_exists": h1_exists,
                    },
                }
            )

        if title_exists is False:
            checks.append(
                {
                    "category": "SEO/UI",
                    "title": (
                        "Проверить требования к Title "
                        "для данной страницы"
                    ),
                    "reason": (
                        "Title отсутствует. Автоматическая проверка "
                        "фиксирует факт, но необходимо подтвердить "
                        "ожидаемое поведение по требованиям проекта."
                    ),
                    "context": {
                        "title_exists": title_exists,
                    },
                }
            )

        return checks

    def _check_images(
        self,
        audit_result: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        checks = []

        images_result = audit_result.get("images", {})

        images_without_alt_count = images_result.get(
            "images_without_alt",
            0,
        )

        images_without_alt = images_result.get(
            "without_alt",
            [],
        )

        if images_without_alt_count:
            checks.append(
                {
                    "category": "Accessibility",
                    "title": (
                        "Проверить необходимость alt "
                        "для найденных изображений"
                    ),
                    "reason": (
                        "Обнаружены изображения без атрибута alt. "
                        "Это может быть проблемой доступности, "
                        "но итоговая оценка зависит от назначения "
                        "изображения: контентное оно или декоративное."
                    ),
                    "context": {
                        "images_without_alt_count": (
                            images_without_alt_count
                        ),
                        "images": images_without_alt,
                    },
                }
            )

        return checks