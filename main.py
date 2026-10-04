from checks.http_checks import check_url
from checks.link_checks import check_page_links
from checks.forms_checks import get_forms
from checks.ui_checks import check_page_title
from report_writer import save_report


def main():
    url = input("Введите URL сайта: ")

    result = check_url(url)

    print("\nРезультат основной проверки:")
    print(f"URL: {result['url']}")
    print(f"Status code: {result['status_code']}")
    print(f"Response time: {result['response_time']} sec")
    print(f"Available: {result['is_available']}")
    print(f"Performance: {result['performance_status']}")

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print("\nПроверка ссылок:")
    links = check_page_links(url)

    if not links:
        print("Ссылки не найдены.")
    else:
        broken_count = 0

        for link in links:
            status = link["status_code"]
            is_broken = link["is_broken"]

            if is_broken:
                broken_count += 1
                result_label = "BROKEN"
            else:
                result_label = "OK"

            print(f"{result_label} | {status} | {link['url']}")

        print("\nИтог по ссылкам:")
        print(f"Всего ссылок: {len(links)}")
        print(f"Битых ссылок: {broken_count}")

    print("\nПроверка форм:")
    forms = get_forms(url)

    if not forms:
        print("Формы не найдены.")
    else:
        print(f"Найдено форм: {len(forms)}")

        for form in forms:
            print(f"\nФорма #{form['form_number']}")
            print(f"Method: {form['method']}")
            print(f"Action: {form['action']}")
            print(f"Количество полей: {len(form['fields'])}")
            print(f"Кнопок submit: {len(form['submit_buttons'])}")

            for field in form["fields"]:
                print(
                    f"- {field['tag']} | "
                    f"type={field['type']} | "
                    f"name={field['name']} | "
                    f"required={field['required']}"
                )

    print("\nUI-проверка через Selenium:")
    ui_result = check_page_title(url)

    print(f"UI status: {ui_result['ui_status']}")
    print(f"Title: {ui_result['title']}")
    print(f"Title exists: {ui_result['title_exists']}")
    print(f"H1 exists: {ui_result['h1_exists']}")
    print(f"H1 text: {ui_result['h1_text']}")

    if "error" in ui_result:
        print(f"UI error: {ui_result['error']}")

    if ui_result.get("screenshot"):
        print(f"Screenshot: {ui_result['screenshot']}")

    report_path = save_report(
        url=url,
        main_result=result,
        links=links,
        forms=forms,
        ui_result=ui_result
    )

    print("\nОтчёт сохранён:")
    print(report_path)


if __name__ == "__main__":
    main()