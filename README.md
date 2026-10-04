# QA Audit Service

QA Audit Service — сервис для автоматизированного технического аудита веб-сайтов.

Проект создан как портфолио-проект Junior QA Engineer и развивается как практический инструмент для базовой технической и UI-проверки веб-сайтов.

## Возможности

Сервис выполняет:

- проверку доступности сайта;
- получение HTTP status code;
- измерение времени HTTP-ответа;
- базовую оценку времени ответа;
- поиск внутренних ссылок;
- нормализацию URL;
- обнаружение битых ссылок;
- поиск HTML-форм;
- анализ полей форм;
- анализ submit-кнопок;
- UI-проверки через Selenium;
- проверку наличия `title`;
- проверку наличия `h1`;
- получение текста `h1`;
- подсчёт ссылок на странице;
- подсчёт кнопок;
- аудит изображений;
- поиск изображений без `alt`;
- автоматическое создание screenshot при UI-ошибке;
- обработку Selenium timeout и WebDriver ошибок;
- автоматическое формирование Markdown-отчёта.

## Логика работы

Пользователь вводит URL сайта.

Сервис последовательно выполняет:

1. HTTP-проверку.
2. Проверку внутренних ссылок.
3. Анализ HTML-форм.
4. Selenium UI-аудит.
5. Проверку изображений.
6. Формирование итогового Markdown-отчёта.

Ошибка отдельного UI-модуля не останавливает весь аудит.

Например, если Selenium получает `Page load timeout`, сервис:

- сохраняет остальные результаты;
- выставляет UI status `ERROR`;
- создаёт screenshot;
- добавляет путь к screenshot в отчёт;
- выставляет общий статус `WARN`.

## Статусы

Используются четыре основных статуса:

- `PASS` — проверка завершена успешно;
- `WARN` — обнаружено предупреждение;
- `FAIL` — критическая проблема;
- `ERROR` — техническая ошибка выполнения отдельной проверки.

Пример:

    UI status: ERROR
    Title:
    Title exists: False
    H1 exists: False
    H1 text:
    Error: Page load timeout
    Screenshot: screenshots/ui_error_2026-10-05_00-33-46.png

## Технологии

- Python
- Requests
- Pytest
- Selenium
- BeautifulSoup4
- Allure Pytest
- Git
- GitHub

## Структура проекта

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
    │   ├── conftest.py
    │   ├── test_http_checks.py
    │   ├── test_link_checks.py
    │   ├── test_forms_checks.py
    │   └── test_ui_checks.py
    │
    ├── reports/
    ├── screenshots/
    │
    ├── audit_report_template.md
    ├── bug_report_template.md
    ├── checklist.md
    ├── config.py
    ├── main.py
    ├── pytest.ini
    ├── report_writer.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## HTTP-проверка

Модуль `http_checks.py` проверяет:

- доступность URL;
- HTTP status code;
- время HTTP-ответа;
- сетевые ошибки.

Базовая классификация времени ответа:

    < 1 сек      PASS
    1–3 сек      WARN
    > 3 сек      FAIL

Важно: это время HTTP-ответа сервера, а не полноценный frontend performance audit и не Core Web Vitals.

## Проверка ссылок

Модуль `link_checks.py`:

- получает ссылки со страницы;
- выбирает внутренние ссылки;
- нормализует URL;
- удаляет fragment;
- приводит scheme и domain к нижнему регистру;
- убирает лишний trailing slash;
- сохраняет query parameters;
- проверяет HTTP status code;
- определяет битые ссылки.

За один аудит проверяется до:

    20 ссылок

Нормализация позволяет избежать дублей вида:

    https://www.python.org
    https://www.python.org/

и:

    https://www.python.org/about
    https://www.python.org/about/

## Проверка форм

Модуль `forms_checks.py` анализирует HTML-формы.

Для каждой формы определяется:

- номер;
- HTTP method;
- action;
- количество полей;
- tag;
- type;
- name;
- наличие `required`;
- количество submit-кнопок.

Пример:

    Форма #1
    Method: GET
    Action: https://www.python.org/search/
    Количество полей: 1
    Кнопок submit: 1
    - input | type=search | name=q | required=False

## Selenium UI-аудит

Модуль `ui_checks.py` запускает Firefox в headless-режиме.

Проверяются:

- загрузка страницы;
- `title`;
- наличие `title`;
- наличие `h1`;
- текст `h1`;
- наличие ссылок;
- количество ссылок;
- наличие кнопок;
- количество кнопок.

Пример успешного результата:

    UI status: PASS
    Title: QA Test
    Title exists: True
    H1 exists: True
    H1 text: Главный заголовок
    Links exist: True
    Links count: 1
    Buttons exist: True
    Buttons count: 1

## Проверка изображений

Сервис анализирует элементы `<img>`.

Определяется:

- общее количество изображений;
- количество изображений с `alt`;
- количество изображений без `alt`;
- список `src` проблемных изображений.

Если найдено изображение без `alt`, UI status становится `WARN`.

Пример:

    Images count: 3
    Images with alt: 2
    Images without alt: 1

## Автотесты

Проект содержит автоматические тесты для:

- HTTP-проверок;
- классификации времени ответа;
- внутренних ссылок;
- нормализации URL;
- битых ссылок;
- HTML-форм;
- Selenium UI-проверок;
- `title`;
- `h1`;
- ссылок;
- кнопок;
- изображений;
- атрибутов `alt`.

Текущий полный набор:

    37 passed

## Unit и integration tests

Тесты разделены на быстрые локальные проверки и сетевые integration tests.

Для integration tests используется marker:

    @pytest.mark.integration

Маркер зарегистрирован в `pytest.ini`.

Запуск только быстрых тестов:

    pytest -v -m "not integration"

Текущий результат:

    25 passed, 12 deselected

Запуск только integration tests:

    pytest -v -m integration

Текущий результат:

    12 passed, 25 deselected

Запуск всего набора:

    pytest -v

## Оптимизация Selenium tests

Selenium UI-тесты используют общий browser fixture из `tests/conftest.py`.

Firefox запускается один раз на тестовую сессию и переиспользуется между UI-тестами.

До оптимизации запуск UI-тестов занимал примерно:

    84–98 секунд

После оптимизации:

    17 passed in 4.33s

Полный тестовый прогон после оптимизации:

    37 passed in 17.25s

Это позволяет заметно сократить время локального запуска тестов и будущего CI pipeline.

## Обработка Selenium ошибок

Если Selenium не может загрузить страницу, сервис не завершает весь аудит аварийно.

Обрабатываются:

- `TimeoutException`;
- `WebDriverException`;
- другие непредвиденные ошибки.

При timeout возвращается структурированный результат:

    UI status: ERROR
    Title:
    Title exists: False
    H1 exists: False
    H1 text:
    Error: Page load timeout

## Screenshots

При UI-ошибке сервис автоматически сохраняет screenshot в каталог:

    screenshots/

Пример:

    screenshots/ui_error_2026-10-05_00-33-46.png

Путь к screenshot добавляется в итоговый audit report.

## Отчёты

После выполнения аудита Markdown-отчёт автоматически сохраняется в:

    reports/

Имя файла содержит дату и время запуска:

    audit_2026-10-05_00-33-47.md

В отчёт входят:

- URL;
- дата проверки;
- общий статус;
- HTTP status code;
- response time;
- результат проверки доступности;
- результат проверки внутренних ссылок;
- найденные битые ссылки;
- данные HTML-форм;
- Selenium UI results;
- `title`;
- `h1`;
- количество ссылок;
- количество кнопок;
- аудит изображений;
- список изображений без `alt`;
- информация об ошибках Selenium;
- путь к screenshot;
- краткое заключение.

## Пример запуска

Запуск проекта:

    python main.py

Программа запросит:

    Введите URL сайта:

Например:

    https://www.python.org

Пример результата HTTP-проверки:

    URL: https://www.python.org
    Status code: 200
    Response time: 0.12 sec
    Available: True
    Performance: PASS

Пример проверки ссылок:

    Всего ссылок: 20
    Битых ссылок: 0

Пример UI-ошибки:

    UI status: ERROR
    Title:
    Title exists: False
    H1 exists: False
    H1 text:
    UI error: Page load timeout
    Screenshot: screenshots/ui_error_2026-10-05_00-33-46.png

## Установка

Клонировать репозиторий:

    git clone https://github.com/dimadvorokovsky/qa-audit-service.git

Перейти в каталог проекта:

    cd qa-audit-service

Создать virtual environment:

    python -m venv venv

Для Windows PowerShell:

    .\venv\Scripts\Activate.ps1

Если PowerShell блокирует запуск скрипта:

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

После этого снова:

    .\venv\Scripts\Activate.ps1

Установить зависимости:

    pip install -r requirements.txt

## Ручное тестирование

Кроме автоматизированных проверок в репозитории находятся:

- `checklist.md` — универсальный QA checklist;
- `bug_report_template.md` — шаблон bug report;
- `audit_report_template.md` — шаблон итогового аудита.

Checklist включает:

- доступность;
- навигацию;
- формы;
- кнопки;
- контент;
- responsive checks;
- пользовательские сценарии;
- negative scenarios;
- UX;
- финализацию QA-аудита.

## Архитектурные решения

В проекте реализованы:

- разделение проверок по модулям;
- отдельный report writer;
- обработка ошибок отдельных модулей;
- structured results через dictionaries;
- URL normalization;
- reusable Selenium driver;
- pytest fixtures;
- unit/integration separation;
- автоматическое сохранение evidence при UI-ошибке.

## Цель проекта

Цель проекта — создать не просто набор учебных автотестов, а самостоятельный QA-инструмент, который можно использовать как основу для реального технического аудита сайтов.

Проект демонстрирует практику работы с:

- manual QA;
- web testing;
- HTTP;
- HTML parsing;
- Selenium;
- Python;
- pytest;
- fixtures;
- error handling;
- test architecture;
- QA reporting;
- Git/GitHub.

## Roadmap после v1.0

После завершения первой стабильной версии возможны:

- GitHub Actions;
- Allure report generation;
- HTML reports;
- PDF reports;
- FastAPI interface;
- история аудитов;
- database;
- Docker;
- параллельная проверка ссылок;
- дополнительные accessibility checks;
- запуск аудитов для реальных пользователей и клиентов.

## Автор

**Dmitry Dvorokovsky**

Junior QA Engineer

GitHub:

https://github.com/dimadvorokovsky
