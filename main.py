from checks.http_checks import check_url
from checks.link_checks import check_page_links
from checks.forms_checks import get_forms
from checks.ui_checks import check_page_title
from report_writer import save_report

from agent.analyzer import AuditAnalyzer
from agent.prioritizer import IssuePrioritizer
from agent.manual_checks import ManualCheckGenerator
from agent.summary_generator import QASummaryGenerator
from agent.bug_report_generator import BugReportGenerator
from agent.report_writer import AgentReportWriter


def build_agent_input(
    main_result,
    links,
    forms,
    ui_result,
):
    """
    Преобразует результаты QA Audit Service
    в единую структуру для AI QA Agent.
    """

    broken_links = [
        {
            "url": link["url"],
            "status_code": link["status_code"],
        }
        for link in links
        if link["is_broken"]
    ]

    audit_result = {
        "http": {
            "available": main_result["is_available"],
            "status_code": main_result["status_code"],
            "response_time": main_result["response_time"],
            "performance": main_result["performance_status"],
        },
        "links": {
            "total_links": len(links),
            "broken_links": broken_links,
        },
        "forms": {
            "forms": forms,
        },
        "ui": {
            "status": ui_result["ui_status"],
            "title": ui_result["title"],
            "title_exists": ui_result["title_exists"],
            "h1_exists": ui_result["h1_exists"],
            "h1_text": ui_result["h1_text"],
            "links_exist": ui_result["links_exist"],
            "links_count": ui_result["links_count"],
            "buttons_exist": ui_result["buttons_exist"],
            "buttons_count": ui_result["buttons_count"],
            "error": ui_result.get("error"),
            "screenshot": ui_result.get("screenshot"),
        },
        "images": {
            "images_count": ui_result["images_count"],
            "images_with_alt": (
                ui_result["images_with_alt_count"]
            ),
            "images_without_alt": (
                ui_result["images_without_alt_count"]
            ),
            "without_alt": ui_result["images_without_alt"],
        },
    }

    return audit_result


def run_qa_agent(audit_result):
    """
    Запускает AI QA Agent поверх результатов
    автоматического аудита.
    """

    analyzer = AuditAnalyzer()
    prioritizer = IssuePrioritizer()
    manual_check_generator = ManualCheckGenerator()
    summary_generator = QASummaryGenerator()
    bug_report_generator = BugReportGenerator()

    issues = analyzer.analyze(audit_result)

    prioritized_issues = prioritizer.prioritize(
        issues
    )

    manual_checks = manual_check_generator.generate(
        audit_result
    )

    summary = summary_generator.generate(
        prioritized_issues,
        manual_checks,
    )

    bug_reports = bug_report_generator.generate(
        prioritized_issues
    )

    return {
        "issues": prioritized_issues,
        "manual_checks": manual_checks,
        "summary": summary,
        "bug_reports": bug_reports,
    }


def print_agent_result(agent_result):
    """
    Выводит результат работы AI QA Agent
    в консоль.
    """

    issues = agent_result["issues"]
    manual_checks = agent_result["manual_checks"]
    summary = agent_result["summary"]
    bug_reports = agent_result["bug_reports"]

    print("\n" + "=" * 60)
    print("AI QA AGENT")
    print("=" * 60)

    print("\n=== CONFIRMED ISSUES ===")
    print(f"Найдено проблем: {len(issues)}")

    for number, issue in enumerate(
        issues,
        start=1,
    ):
        print()
        print(
            f"{number}. "
            f"[{issue['priority']}] "
            f"[{issue['category']}] "
            f"{issue['title']}"
        )
        print(
            f"   {issue['description']}"
        )
        print(
            f"   Evidence: {issue['evidence']}"
        )

    print("\n=== MANUAL CHECKS ===")
    print(
        f"Проверок вручную: "
        f"{len(manual_checks)}"
    )

    for number, check in enumerate(
        manual_checks,
        start=1,
    ):
        print()
        print(
            f"{number}. "
            f"[{check['category']}] "
            f"{check['title']}"
        )
        print(
            f"   Причина: {check['reason']}"
        )
        print(
            f"   Context: {check['context']}"
        )

    print("\n=== QA SUMMARY ===")
    print()
    print(summary)

    print("\n=== BUG REPORTS ===")
    print(
        f"Создано черновиков: "
        f"{len(bug_reports)}"
    )

    for bug in bug_reports:
        print()
        print(
            f"{bug['id']} — "
            f"{bug['title']}"
        )
        print(
            f"Category: {bug['category']}"
        )
        print(
            f"Priority: {bug['priority']}"
        )

        print("\nPreconditions:")

        for item in bug["preconditions"]:
            print(f"- {item}")

        print("\nSteps:")

        for number, step in enumerate(
            bug["steps"],
            start=1,
        ):
            print(
                f"{number}. {step}"
            )

        print("\nExpected result:")
        print(
            bug["expected_result"]
        )

        print("\nActual result:")
        print(
            bug["actual_result"]
        )

        print("\nEvidence:")
        print(
            bug["evidence"]
        )

        print()
        print("-" * 60)


def main():
    url = input("Введите URL сайта: ")

    result = check_url(url)

    print("\nРезультат основной проверки:")
    print(f"URL: {result['url']}")
    print(
        f"Status code: "
        f"{result['status_code']}"
    )
    print(
        f"Response time: "
        f"{result['response_time']} sec"
    )
    print(
        f"Available: "
        f"{result['is_available']}"
    )
    print(
        f"Performance: "
        f"{result['performance_status']}"
    )

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

            print(
                f"{result_label} | "
                f"{status} | "
                f"{link['url']}"
            )

        print("\nИтог по ссылкам:")
        print(
            f"Всего ссылок: "
            f"{len(links)}"
        )
        print(
            f"Битых ссылок: "
            f"{broken_count}"
        )

    print("\nПроверка форм:")

    forms = get_forms(url)

    if not forms:
        print("Формы не найдены.")
    else:
        print(
            f"Найдено форм: "
            f"{len(forms)}"
        )

        for form in forms:
            print(
                f"\nФорма "
                f"#{form['form_number']}"
            )
            print(
                f"Method: "
                f"{form['method']}"
            )
            print(
                f"Action: "
                f"{form['action']}"
            )
            print(
                f"Количество полей: "
                f"{len(form['fields'])}"
            )
            print(
                f"Кнопок submit: "
                f"{len(form['submit_buttons'])}"
            )

            if form.get("instances", 1) > 1:
                print(
                    f"Экземпляров в DOM: "
                    f"{form['instances']}"
                )

            for field in form["fields"]:
                print(
                    f"- {field['tag']} | "
                    f"type={field['type']} | "
                    f"name={field['name']} | "
                    f"required="
                    f"{field['required']}"
                )

    print("\nUI-проверка через Selenium:")

    ui_result = check_page_title(url)

    print(
        f"UI status: "
        f"{ui_result['ui_status']}"
    )
    print(
        f"Title: "
        f"{ui_result['title']}"
    )
    print(
        f"Title exists: "
        f"{ui_result['title_exists']}"
    )
    print(
        f"H1 exists: "
        f"{ui_result['h1_exists']}"
    )
    print(
        f"H1 text: "
        f"{ui_result['h1_text']}"
    )
    print(
        f"Links exist: "
        f"{ui_result['links_exist']}"
    )
    print(
        f"Links count: "
        f"{ui_result['links_count']}"
    )
    print(
        f"Buttons exist: "
        f"{ui_result['buttons_exist']}"
    )
    print(
        f"Buttons count: "
        f"{ui_result['buttons_count']}"
    )

    print("\nПроверка изображений:")

    print(
        f"Images count: "
        f"{ui_result['images_count']}"
    )
    print(
        f"Images with alt: "
        f"{ui_result['images_with_alt_count']}"
    )
    print(
        f"Images without alt: "
        f"{ui_result['images_without_alt_count']}"
    )

    if ui_result["images_without_alt"]:
        print("Изображения без alt:")

        for image_src in (
            ui_result["images_without_alt"]
        ):
            print(f"- {image_src}")

    if "error" in ui_result:
        print(
            f"UI error: "
            f"{ui_result['error']}"
        )

    if ui_result.get("screenshot"):
        print(
            f"Screenshot: "
            f"{ui_result['screenshot']}"
        )

    report_path = save_report(
        url=url,
        main_result=result,
        links=links,
        forms=forms,
        ui_result=ui_result,
    )

    print("\nОтчёт QA Audit Service сохранён:")
    print(report_path)

    audit_result = build_agent_input(
        main_result=result,
        links=links,
        forms=forms,
        ui_result=ui_result,
    )

    agent_result = run_qa_agent(
        audit_result
    )

    print_agent_result(
        agent_result
    )

    agent_report_writer = AgentReportWriter()

    agent_report_path = agent_report_writer.save(
        url=url,
        agent_result=agent_result,
    )

    print("\nОтчёт AI QA Agent сохранён:")
    print(agent_report_path)


if __name__ == "__main__":
    main()