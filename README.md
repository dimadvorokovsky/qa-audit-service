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
- группировку битых ссылок по проблемным URL-веткам;
- поиск HTML-форм;
- анализ полей форм;
- анализ submit-кнопок;
- дедупликацию одинаковых форм;
- подсчёт количества экземпляров одинаковой формы в DOM;
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

```text
UI status: ERROR
Title:
Title exists: False
H1 exists: False
H1 text:
Error: Page load timeout
Screenshot: screenshots/ui_error_2026-10-05_00-33-46.png
```


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
├── examples/
│   └── filsnab.ru/
│       ├── README.md
│       └── audit.md
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
```


## HTTP-проверка

Модуль `http_checks.py` проверяет:

- доступность URL;
- HTTP status code;
- время HTTP-ответа;
- сетевые ошибки.

Базовая классификация времени ответа:

```text
< 1 сек      PASS
1–3 сек      WARN
> 3 сек      FAIL
```

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

```text
20 ссылок
```

Нормализация позволяет избежать дублей вида:

```text
https://www.python.org
https://www.python.org/
```

и:

```text
https://www.python.org/about
https://www.python.org/about/
```

В Markdown-отчёте битые ссылки дополнительно группируются по проблемным URL-веткам.

Например:

```text
/catalog/filtratsiya — 7 битых ссылок
/catalog/filtratsiyaa — 7 битых ссылок
/blogg — 1 битая ссылка
```


## Проверка форм

Модуль `forms_checks.py` анализирует HTML-формы.

Для каждой формы определяется:

- HTTP method;
- action;
- количество полей;
- tag;
- type;
- name;
- наличие `required`;
- количество submit-кнопок.

Одинаковые формы группируются по:

- method;
- action;
- набору полей.

Если одинаковая форма встречается в DOM несколько раз, сервис выводит её один раз и отдельно указывает количество экземпляров.

Пример:

```text
Форма #1
Экземпляров: 4
Method: GET
Action: https://filsnab.ru/catalog/
Количество полей в одном экземпляре: 2
Submit-кнопок в одном экземпляре: 1

- input | type=text | name=q | required=False
- input | type=hidden | name=type | required=False
```


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

```text
UI status: PASS
Title: QA Test
Title exists: True
H1 exists: True
H1 text: Главный заголовок
Links exist: True
Links count: 1
Buttons exist: True
Buttons count: 1
```


## Проверка изображений

Сервис анализирует элементы `<img>`.

Определяется:

- общее количество изображений;
- количество изображений с `alt`;
- количество изображений без `alt`;
- список `src` проблемных изображений.

Если найдено изображение без `alt`, UI status становится `WARN`.

Пример:

```text
Images count: 3
Images with alt: 2
Images without alt: 1
```


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

```text
37 passed
```


## Unit и integration tests

Тесты разделены на быстрые локальные проверки и сетевые integration tests.

Для integration tests используется marker:

```python
@pytest.mark.integration
```

Маркер зарегистрирован в `pytest.ini`.

Запуск только быстрых тестов:

```bash
pytest -v -m "not integration"
```

Текущий результат:

```text
25 passed, 12 deselected
```

Запуск только integration tests:

```bash
pytest -v -m integration
```

Текущий результат:

```text
12 passed, 25 deselected
```

Запуск всего набора:

```bash
pytest -v
```


## Оптимизация Selenium tests

Selenium UI-тесты используют общий browser fixture из `tests/conftest.py`.

Firefox запускается один раз на тестовую сессию и переиспользуется между UI-тестами.

До оптимизации запуск UI-тестов занимал примерно:

```text
84–98 секунд
```

После оптимизации:

```text
17 passed in 4.33s
```

Полный тестовый прогон после оптимизации:

```text
37 passed in 17.25s
```

Это позволяет заметно сократить время локального запуска тестов и будущего CI pipeline.


## Обработка Selenium ошибок

Если Selenium не может загрузить страницу, сервис не завершает весь аудит аварийно.

Обрабатываются:

- `TimeoutException`;
- `WebDriverException`;
- другие непредвиденные ошибки.

При timeout возвращается структурированный результат:

```text
UI status: ERROR
Title:
Title exists: False
H1 exists: False
H1 text:
Error: Page load timeout
```


## Screenshots

При UI-ошибке сервис автоматически сохраняет screenshot в каталог:

```text
screenshots/
```

Пример:

```text
screenshots/ui_error_2026-10-05_00-33-46.png
```

Путь к screenshot добавляется в итоговый audit report.


## Отчёты

После выполнения аудита Markdown-отчёт автоматически сохраняется в:

```text
reports/
```

Имя файла содержит дату и время запуска:

```text
audit_2026-10-05_00-33-47.md
```

В отчёт входят:

- URL;
- дата проверки;
- общий статус;
- HTTP status code;
- response time;
- результат проверки доступности;
- результат проверки внутренних ссылок;
- группировка проблемных URL-веток;
- полный список найденных битых ссылок;
- количество уникальных форм;
- количество экземпляров одинаковых форм в DOM;
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

```bash
python main.py
```

Программа запросит:

```text
Введите URL сайта:
```

Например:

```text
https://www.python.org
```

Пример результата HTTP-проверки:

```text
URL: https://www.python.org
Status code: 200
Response time: 0.12 sec
Available: True
Performance: PASS
```

Пример проверки ссылок:

```text
Всего ссылок: 20
Битых ссылок: 0
```

Пример UI-ошибки:

```text
UI status: ERROR
Title:
Title exists: False
H1 exists: False
H1 text:
UI error: Page load timeout
Screenshot: screenshots/ui_error_2026-10-05_00-33-46.png
```


## Установка

Клонировать репозиторий:

```bash
git clone https://github.com/dimadvorokovsky/qa-audit-service.git
```

Перейти в каталог проекта:

```bash
cd qa-audit-service
```

Создать virtual environment:

```bash
python -m venv venv
```

Для Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Если PowerShell блокирует запуск скрипта:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

После этого снова:

```powershell
.\venv\Scripts\Activate.ps1
```

Для Windows CMD:

```bat
venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```


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
- автоматическое сохранение evidence при UI-ошибке;
- дедупликация одинаковых HTML-форм;
- группировка битых ссылок по URL-веткам.


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


## Real-world audit case: filsnab.ru

QA Audit Service был протестирован на реальном веб-сайте:

```text
https://filsnab.ru/
```

Цель проверки — не только найти технические проблемы сайта, но и проверить сам QA Audit Service в условиях реального проекта.


### Результат контрольного прогона

```text
Status Code: 200 OK
Response time: 0.187 sec
Performance: PASS

Проверено внутренних ссылок: 20
Найдено битых ссылок: 16

Уникальных форм: 1
Экземпляров формы в DOM: 4

UI status: WARN
Title exists: True
H1 exists: False

Images count: 15
Images without alt: 1
```


### Найденные проблемные URL-ветки

```text
/catalog/filtratsiya — 7 битых ссылок
/catalog/filtratsiyaa — 7 битых ссылок
/blogg — 1 битая ссылка
/catalog/gidravlika — 1 битая ссылка
```

Дополнительно:

- на главной странице не обнаружен `H1`;
- у одного изображения отсутствует `alt`.


### Что было улучшено после реального аудита

Первый аудит реального сайта выявил недостатки не только сайта, но и самого QA Audit Service.

До доработки сервис выводил четыре одинаковые формы как четыре отдельных результата.

После анализа была реализована дедупликация форм.

Теперь отчёт показывает:

```text
Уникальных форм: 1
Всего экземпляров форм в DOM: 4
```

Также был улучшен анализ битых ссылок.

Вместо только длинного списка 404 сервис теперь дополнительно формирует компактную сводку по проблемным URL-веткам.

Были добавлены:

- дедупликация одинаковых форм;
- подсчёт экземпляров формы в DOM;
- группировка битых URL по проблемным веткам;
- сохранение полного списка 404;
- улучшенная структура Markdown-отчёта;
- корректное склонение количества битых ссылок.


### Цикл работы над кейсом

```text
реальный сайт
→ автоматический аудит
→ анализ результатов
→ выявление недостатков самого инструмента
→ доработка QA Audit Service
→ повторное тестирование
→ контрольный прогон
```

Таким образом, кейс демонстрирует не только запуск готового инструмента, но и полный QA-цикл с анализом результатов и улучшением продукта на основании реальных данных.


### Материалы кейса

Описание:

[`examples/filsnab.ru/README.md`](examples/filsnab.ru/README.md)

Финальный Markdown-отчёт:

[`examples/filsnab.ru/audit.md`](examples/filsnab.ru/audit.md)


## Roadmap после v1.0

После завершения первой стабильной версии возможны:

- AI QA Agent;
- GitHub Actions;
- Allure report generation;
- HTML reports;
- PDF reports;
- FastAPI interface;
- история аудитов;
- database;
- Docker;
- параллельная проверка ссылок;
- дополнительные accessibility-проверки;
- запуск аудитов для реальных пользователей и клиентов.


## Автор

**Dmitry Dvorokovsky**

Junior QA Engineer

GitHub:

https://github.com/dimadvorokovsky