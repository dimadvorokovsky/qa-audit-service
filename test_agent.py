from agent.analyzer import AuditAnalyzer
from agent.prioritizer import IssuePrioritizer
from agent.manual_checks import ManualCheckGenerator
from agent.summary_generator import QASummaryGenerator
from agent.bug_report_generator import BugReportGenerator


audit_result = {
    "http": {
        "available": True,
        "status_code": 200,
        "response_time": 0.187,
        "performance": "PASS",
    },
    "links": {
        "broken_links": [
            "https://filsnab.ru/blogg",
            "https://filsnab.ru/catalog/gidravlika",
        ]
    },
    "ui": {
        "status": "WARN",
        "title_exists": True,
        "h1_exists": False,
        "error": None,
    },
    "images": {
        "images_without_alt": 1,
        "without_alt": [
            "https://partners.aspro.ru/upload/iblock/example.png"
        ],
    },
    "forms": {
        "forms": [
            {
                "method": "GET",
                "action": "https://filsnab.ru/catalog/",
                "instances": 4,
                "fields": [
                    {
                        "tag": "input",
                        "type": "text",
                        "name": "q",
                        "required": False,
                    },
                    {
                        "tag": "input",
                        "type": "hidden",
                        "name": "type",
                        "required": False,
                    },
                ],
            }
        ]
    },
}


analyzer = AuditAnalyzer()
prioritizer = IssuePrioritizer()
manual_check_generator = ManualCheckGenerator()
summary_generator = QASummaryGenerator()
bug_report_generator = BugReportGenerator()

issues = analyzer.analyze(audit_result)
prioritized_issues = prioritizer.prioritize(issues)
manual_checks = manual_check_generator.generate(audit_result)

summary = summary_generator.generate(
    prioritized_issues,
    manual_checks,
)

bug_reports = bug_report_generator.generate(
    prioritized_issues,
)


print("=== CONFIRMED ISSUES ===")
print(f"Найдено проблем: {len(prioritized_issues)}")
print()

for number, issue in enumerate(prioritized_issues, start=1):
    print(
        f"{number}. "
        f"[{issue['priority']}] "
        f"[{issue['category']}] "
        f"{issue['title']}"
    )
    print(f"   {issue['description']}")
    print(f"   Evidence: {issue['evidence']}")
    print()


print("=== MANUAL CHECKS ===")
print(f"Проверок вручную: {len(manual_checks)}")
print()

for number, check in enumerate(manual_checks, start=1):
    print(
        f"{number}. "
        f"[{check['category']}] "
        f"{check['title']}"
    )
    print(f"   Причина: {check['reason']}")
    print(f"   Context: {check['context']}")
    print()


print("=== QA SUMMARY ===")
print()
print(summary)
print()


print("=== BUG REPORTS ===")
print(f"Создано черновиков: {len(bug_reports)}")
print()

for bug in bug_reports:
    print(f"{bug['id']} — {bug['title']}")
    print(f"Category: {bug['category']}")
    print(f"Priority: {bug['priority']}")
    print()

    print("Preconditions:")
    for item in bug["preconditions"]:
        print(f"- {item}")

    print()
    print("Steps:")
    for number, step in enumerate(bug["steps"], start=1):
        print(f"{number}. {step}")

    print()
    print("Expected result:")
    print(bug["expected_result"])

    print()
    print("Actual result:")
    print(bug["actual_result"])

    print()
    print("Evidence:")
    print(bug["evidence"])

    print()
    print("-" * 60)
    print()