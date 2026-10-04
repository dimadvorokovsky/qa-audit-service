from datetime import datetime
from pathlib import Path


def get_overall_status(main_result, broken_links):
    if not main_result["is_available"]:
        return "FAIL"

    if broken_links:
        return "WARN"

    if main_result["performance_status"] == "FAIL":
        return "WARN"

    return "PASS"


def save_report(url, main_result, links, forms):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = reports_dir / f"audit_{timestamp}.md"

    broken_links = [
        link for link in links
        if link["is_broken"]
    ]

    overall_status = get_overall_status(
        main_result,
        broken_links
    )

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("# QA Audit Report\n\n")

        file.write("## Общая информация\n\n")
        file.write(f"- URL: {url}\n")
        file.write(
            f"- Дата проверки: "
            f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        )
        file.write(
            f"- Общий статус: **{overall_status}**\n\n"
        )

        file.write("## Основная проверка\n\n")
        file.write(
            f"- Status code: {main_result['status_code']}\n"
        )
        file.write(
            f"- Response time: {main_result['response_time']} sec\n"
        )
        file.write(
            f"- Available: {main_result['is_available']}\n"
        )
        file.write(
            f"- Performance: "
            f"{main_result['performance_status']}\n\n"
        )

        file.write("## Проверка ссылок\n\n")
        file.write(
            f"- Проверено ссылок: {len(links)}\n"
        )
        file.write(
            f"- Битых ссылок: {len(broken_links)}\n"
        )

        if broken_links:
            file.write(
                "- Результат: **Найдены проблемные ссылки**\n\n"
            )

            file.write("### Битые ссылки\n\n")

            for link in broken_links:
                file.write(
                    f"- {link['status_code']} | "
                    f"{link['url']}\n"
                )

            file.write("\n")

        else:
            file.write(
                "- Результат: **Проблем не обнаружено**\n\n"
            )

        file.write("## Проверка форм\n\n")
        file.write(
            f"- Найдено форм: {len(forms)}\n"
        )

        total_fields = sum(
            len(form["fields"])
            for form in forms
        )

        total_submit_buttons = sum(
            len(form["submit_buttons"])
            for form in forms
        )

        file.write(
            f"- Всего полей: {total_fields}\n"
        )
        file.write(
            f"- Submit-кнопок: {total_submit_buttons}\n\n"
        )

        for form in forms:
            file.write(
                f"### Форма #{form['form_number']}\n\n"
            )
            file.write(
                f"- Method: {form['method']}\n"
            )
            file.write(
                f"- Action: {form['action']}\n"
            )
            file.write(
                f"- Количество полей: "
                f"{len(form['fields'])}\n"
            )
            file.write(
                f"- Submit-кнопок: "
                f"{len(form['submit_buttons'])}\n\n"
            )

            if form["fields"]:
                file.write("#### Поля формы\n\n")

                for field in form["fields"]:
                    file.write(
                        f"- {field['tag']} | "
                        f"type={field['type']} | "
                        f"name={field['name']} | "
                        f"required={field['required']}\n"
                    )

                file.write("\n")

        file.write("## Краткое заключение\n\n")

        if overall_status == "PASS":
            file.write(
                "Автоматические проверки завершены успешно. "
                "Критических технических проблем в рамках "
                "выполненных проверок не обнаружено.\n"
            )

        elif overall_status == "WARN":
            file.write(
                "Автоматические проверки завершены с "
                "предупреждениями. Рекомендуется изучить "
                "найденные проблемы подробнее.\n"
            )

        else:
            file.write(
                "Автоматические проверки выявили критическую "
                "проблему с доступностью сайта.\n"
            )

    return str(file_path)