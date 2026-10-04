# QA Audit Service

QA Audit Service — учебно-практический сервис для автоматизированного технического аудита веб-сайтов.

Проект создан как портфолио-проект Junior QA Engineer и развивается как полноценный инструмент для базовой проверки сайтов.

## Что умеет сервис

Сейчас сервис выполняет следующие проверки:

- доступность сайта;
- HTTP status code;
- время ответа сервера;
- базовую оценку производительности по времени ответа;
- проверку внутренних ссылок;
- обнаружение битых ссылок;
- поиск HTML-форм;
- анализ полей форм;
- анализ submit-кнопок;
- UI-проверку через Selenium;
- проверку наличия title страницы;
- обработку Selenium timeout и WebDriver ошибок;
- автоматическое формирование Markdown-отчёта.

## Общая логика работы

Пользователь вводит URL сайта.

После этого сервис последовательно выполняет:

1. HTTP-проверку.
2. Проверку внутренних ссылок.
3. Анализ форм.
4. UI-проверку через Selenium.
5. Формирование итогового отчёта.

Если один из UI-модулей завершается ошибкой, например возникает Selenium timeout, весь аудит не завершается аварийно.

Ошибка фиксируется в результате проверки, а итоговый отчёт всё равно создаётся.

## Статусы

Для результатов используются статусы:

- `PASS` — проверка прошла успешно;
- `WARN` — обнаружено предупреждение;
- `FAIL` — критическая проблема;
- `ERROR` — техническая ошибка выполнения отдельной проверки.

Пример:

```text
UI status: ERROR
Title:
Title exists: False
UI error: Page load timeout
```

При этом общий аудит продолжает работу и формирует отчёт.

## Технологии

Проект использует:

- Python
- Requests
- Pytest
- Selenium
- BeautifulSoup4
- Allure Pytest
- Git
- GitHub

## Структура проекта

```text
qa-audit-service/
│
├── checks/
│   ├── __init__.py
│   ├── http_checks.py
│   ├── link_checks.py
│   ├── forms_checks.py
│   └── ui_checks.py
│
├── tests/
│   ├── __init__.py
│   ├── test_http_checks.py
│   ├── test_link_checks.py
│   ├── test_forms_checks.py
│   └── test_ui_checks.py
│
├── reports/
├── screenshots/
├── audit_report_template.md
├── bug_report_template.md
├── checklist.md
├── config.py
├── main.py
├── report_writer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## HTTP-проверка

Модуль `http_checks.py` проверяет:

- доступность URL;
- HTTP status code;
- время ответа;
- наличие сетевой ошибки.

Также используется базовая классификация времени ответа:

```text
< 1 сек      PASS
1–3 сек      WARN
> 3 сек      FAIL
```

Важно: это время HTTP-ответа, а не полноценный анализ производительности страницы и не Core Web Vitals.

## Проверка ссылок

Модуль `link_checks.py`:

- получает ссылки со страницы;
- выбирает внутренние ссылки;
- удаляет fragment из URL;
- проверяет HTTP status code;
- определяет битые ссылки.

Чтобы аудит не выполнялся слишком долго, за один запуск проверяется ограниченное количество ссылок.

Текущий лимит:

```text
20 ссылок
```

## Проверка форм

Модуль `forms_checks.py` анализирует HTML-формы страницы.

Для каждой формы определяется:

- номер формы;
- HTTP method;
- action;
- количество полей;
- тип поля;
- имя поля;
- наличие атрибута required;
- наличие submit-кнопок.

Пример:

```text
Форма #1
Method: GET
Action: https://www.python.org/search/
Количество полей: 1
Кнопок submit: 1
- input | type=search | name=q | required=False
```

## UI-проверка через Selenium

Модуль `ui_checks.py` запускает Firefox через Selenium в headless-режиме.

Сейчас проверяется:

- возможность открыть страницу;
- наличие title;
- значение title.

Пример успешного результата:

```text
UI status: PASS
Title: Welcome to Python.org
Title exists: True
```

Если страница не загрузилась за установленное время:

```text
UI status: ERROR
Title:
Title exists: False
Error: Page load timeout
```

При этом остальные результаты аудита не теряются.

## Автотесты

Проект содержит автотесты для:

- HTTP-проверок;
- классификации времени ответа;
- проверки ссылок;
- определения битых ссылок;
- анализа форм;
- UI-проверки через Selenium.

UI-тесты используют локальную HTML-страницу через `data:` URL.

Это сделано специально, чтобы автотесты не зависели от доступности внешнего сайта и интернет-соединения.

Запуск всех тестов:

```bash
pytest -v
```

Запуск только UI-тестов:

```bash
pytest tests/test_ui_checks.py -v
```

На текущем этапе:

```text
17 passed
```

## Почему UI-тесты не используют реальный сайт

Ранее UI-тесты запускались на `https://www.python.org`.

Это делало тесты зависимыми от:

- интернета;
- скорости внешнего сайта;
- браузера;
- сетевых задержек.

В результате корректный код мог получить ложное падение из-за `Page load timeout`.

Поэтому тестирование собственной логики было отделено от интеграционной проверки реального сайта.

## Запуск проекта

Клонировать репозиторий:

```bash
git clone https://github.com/dimadvorokovsky/qa-audit-service.git
```

Перейти в каталог:

```bash
cd qa-audit-service
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активировать его в Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Если PowerShell запрещает выполнение скрипта:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

После этого снова:

```powershell
.\venv\Scripts\Activate.ps1
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Запустить аудит:

```bash
python main.py
```

После запуска программа запросит URL:

```text
Введите URL сайта:
```

Например:

```text
https://www.python.org
```

## Пример результата

Пример HTTP-проверки:

```text
URL: https://www.python.org
Status code: 200
Response time: 0.125 sec
Available: True
Performance: PASS
```

Пример проверки ссылок:

```text
Всего ссылок: 20
Битых ссылок: 0
```

Пример проверки формы:

```text
Найдено форм: 1

Форма #1
Method: GET
Action: https://www.python.org/search/
Количество полей: 1
Кнопок submit: 1
```

Пример UI-проверки при timeout:

```text
UI status: ERROR
Title:
Title exists: False
UI error: Page load timeout
```

## Отчёт

После завершения аудита Markdown-отчёт автоматически сохраняется в:

```text
reports/
```

Имя файла содержит дату и время запуска:

```text
audit_2026-10-04_23-40-07.md
```

Пример содержимого:

```text
# QA Audit Report

## Общая информация

- URL: https://www.python.org
- Общий статус: WARN

## Основная проверка

- Status code: 200
- Response time: 0.125 sec
- Available: True
- Performance: PASS

## Проверка ссылок

- Проверено ссылок: 20
- Битых ссылок: 0

## UI-проверка через Selenium

- UI status: ERROR
- Title:
- Title exists: False
- Error: Page load timeout
```

## Ручное тестирование

Кроме автоматизированных проверок в проект входят:

- универсальный QA-чек-лист;
- шаблон bug report;
- шаблон итогового audit report.

Файл `checklist.md` содержит проверки:

- доступности;
- навигации;
- форм;
- кнопок;
- контента;
- адаптивности;
- пользовательских сценариев;
- негативных сценариев;
- UX;
- финального оформления аудита.

## Цель проекта

Основная цель — создать не только учебный набор автотестов, а развиваемый QA-инструмент, который можно использовать для реального технического аудита сайтов.

Проект позволяет практиковать:

- manual QA;
- web testing;
- HTTP;
- автоматизацию;
- Selenium;
- Python;
- pytest;
- обработку ошибок;
- построение тестовой архитектуры;
- создание QA-отчётности;
- Git/GitHub.

## Roadmap

План дальнейшего развития:

- расширение Selenium UI-проверок;
- smoke UI scenarios;
- browser-based form checks;
- автоматические screenshots;
- улучшение обработки ошибок модулей;
- нормализация URL;
- параллельная проверка ссылок;
- разделение unit и integration tests;
- pytest fixtures для браузера;
- Allure reports;
- HTML report;
- PDF report;
- web interface;
- FastAPI;
- история аудитов;
- база данных;
- GitHub Actions;
- Docker;
- запуск на реальных клиентских сайтах.

## Автор

**Dmitry Dvorokovsky**

Junior QA Engineer

GitHub:

https://github.com/dimadvorokovsky
