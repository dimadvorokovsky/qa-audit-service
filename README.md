# QA Audit Service

QA Audit Service — инструмент для базового автоматизированного аудита веб-сайтов.

Проект создан как собственный QA-инструмент для проверки доступности сайта, внутренних ссылок, форм и формирования структурированного отчёта по результатам аудита.

## Цель проекта

Создать сервис, который помогает быстро проводить первичную техническую проверку сайта и формировать понятный QA-отчёт.

Проект сочетает автоматические проверки и ручной QA-аудит.

## Возможности

### HTTP-проверки

- Проверка доступности сайта
- Получение HTTP status code
- Измерение времени ответа
- Оценка производительности:
  - PASS — менее 1 секунды
  - WARN — от 1 до 3 секунд
  - FAIL — более 3 секунд

### Проверка ссылок

- Поиск внутренних ссылок на странице
- Проверка HTTP-статуса каждой ссылки
- Определение битых ссылок
- Ограничение количества проверяемых ссылок для быстрого аудита

### Проверка форм

- Поиск форм на странице
- Определение метода формы GET / POST
- Определение action
- Поиск полей input / textarea / select
- Проверка наличия required
- Поиск submit-кнопок

### Отчёты

После проверки автоматически создаётся Markdown-отчёт.

Отчёт содержит:

- URL сайта
- дату проверки
- общий статус
- HTTP status code
- response time
- performance status
- количество проверенных ссылок
- количество битых ссылок
- информацию о найденных формах
- краткое заключение

## Ручной QA-аудит

В проект также входят шаблоны для ручной проверки:

- `checklist.md` — универсальный QA-чек-лист
- `bug_report_template.md` — шаблон баг-репорта
- `audit_report_template.md` — шаблон итогового QA-отчёта

## Technology Stack

- Python
- Requests
- Pytest
- Selenium
- BeautifulSoup
- Allure
- Git
- GitHub

## Структура проекта

```text
qa-audit-service/
│
├── checks/
│   ├── http_checks.py
│   ├── link_checks.py
│   ├── forms_checks.py
│   └── ui_checks.py
│
├── tests/
│   ├── test_http_checks.py
│   ├── test_link_checks.py
│   └── test_forms_checks.py
│
├── reports/
│
├── screenshots/
│
├── main.py
├── report_writer.py
├── config.py
├── checklist.md
├── bug_report_template.md
├── audit_report_template.md
├── requirements.txt
└── README.md