\# QA Audit Service + AI QA Agent



QA Audit Service — Python-сервис для автоматизированного технического и UI-аудита веб-сайтов.



Проект создан как портфолио-проект Junior QA Engineer и развивается как практический QA-инструмент для технического анализа сайтов, формирования отчётов и последующей автоматизированной обработки результатов.



Поверх QA Audit Service реализован \*\*AI QA Agent Core\*\*, который получает структурированные результаты аудита, выделяет подтверждённые технические проблемы, назначает приоритеты, формирует manual checks, QA Summary и черновики bug reports.



> Текущая версия агента использует детерминированную rule-based логику. Подключение LLM-слоя для дополнительного анализа предусмотрено как дальнейшее развитие проекта.





\## Возможности QA Audit Service



Сервис выполняет:



\- проверку доступности сайта;

\- получение HTTP status code;

\- измерение времени HTTP-ответа;

\- базовую оценку времени ответа;

\- поиск внутренних ссылок;

\- нормализацию URL;

\- обнаружение битых ссылок;

\- группировку битых ссылок по проблемным URL-веткам;

\- поиск HTML-форм;

\- анализ полей форм;

\- анализ submit-кнопок;

\- дедупликацию одинаковых форм;

\- подсчёт количества экземпляров одинаковой формы в DOM;

\- UI-проверки через Selenium;

\- проверку наличия `title`;

\- проверку наличия `h1`;

\- получение текста `h1`;

\- подсчёт ссылок на странице;

\- подсчёт кнопок;

\- аудит изображений;

\- поиск изображений без `alt`;

\- автоматическое создание screenshot при UI-ошибке;

\- обработку Selenium timeout и WebDriver ошибок;

\- автоматическое формирование Markdown-отчёта.





\## Возможности AI QA Agent



После завершения технического аудита результаты автоматически передаются агенту.



AI QA Agent Core выполняет:



\- анализ структурированных результатов аудита;

\- выделение подтверждённых технических проблем;

\- приоритизацию `CRITICAL / HIGH / MEDIUM / LOW`;

\- формирование списка проверок, требующих ручного QA-анализа;

\- отделение подтверждённых дефектов от потенциально спорных находок;

\- формирование QA Summary;

\- генерацию черновиков bug reports;

\- сохранение Evidence;

\- создание отдельного Markdown-отчёта агента.





\## Общая логика работы



```text

URL сайта

↓

QA Audit Service

↓

HTTP / Links / Forms / Selenium / Images

↓

структурированный результат аудита

↓

технический Markdown-отчёт

↓

AI QA Agent Core

↓

Confirmed Issues

↓

Prioritization

↓

Manual Checks

↓

QA Summary

↓

Bug Report Drafts

↓

Agent Markdown Report

```





\## QA-подход агента



Агент не объявляет каждую найденную особенность багом автоматически.



Подтверждёнными проблемами считаются технические факты, которые можно доказать результатами проверки.



Например:



```text

внутренняя ссылка возвращает HTTP 404

→ confirmed issue

```



Находки, которые зависят от требований, назначения элемента или бизнес-логики, направляются в `Manual Checks`.



Например:



```text

отсутствует H1

→ проверить требования к конкретному типу страницы



изображение без alt

→ проверить, является ли изображение контентным или декоративным



у формы отсутствует required

→ проверить бизнес-логику формы

```



Такой подход уменьшает количество false positive и отделяет автоматически подтверждённые дефекты от ситуаций, которые требуют решения QA-инженера.





\## Статусы QA Audit Service



Используются четыре основных статуса:



\- `PASS` — проверка завершена успешно;

\- `WARN` — обнаружено предупреждение;

\- `FAIL` — критическая проблема;

\- `ERROR` — техническая ошибка выполнения отдельной проверки.



Пример:



```text

UI status: ERROR

Title:

Title exists: False

H1 exists: False

H1 text:

Error: Page load timeout

Screenshot: screenshots/ui\_error\_2026-10-05\_00-33-46.png

```





\## Приоритеты AI QA Agent



Агент использует четыре уровня приоритета:



```text

CRITICAL

HIGH

MEDIUM

LOW

```



Пример:



```text

16 внутренних ссылок возвращают HTTP 404

→ HIGH

```



Приоритет назначается на основании типа проблемы и её масштаба.





\## Технологии



\- Python

\- Requests

\- BeautifulSoup4

\- Selenium WebDriver

\- Pytest

\- Allure Pytest

\- Markdown

\- Git

\- GitHub





\## Структура проекта



```text

qa-audit-service/

│

├── agent/

│   ├── \_\_init\_\_.py

│   ├── analyzer.py

│   ├── prioritizer.py

│   ├── manual\_checks.py

│   ├── summary\_generator.py

│   ├── bug\_report\_generator.py

│   └── report\_writer.py

│

├── checks/

│   ├── \_\_init\_\_.py

│   ├── http\_checks.py

│   ├── link\_checks.py

│   ├── forms\_checks.py

│   └── ui\_checks.py

│

├── examples/

│   ├── ai-qa-agent/

│   │   ├── README.md

│   │   └── agent\_report.md

│   │

│   └── filsnab.ru/

│       ├── README.md

│       └── audit.md

│

├── tests/

│   ├── \_\_init\_\_.py

│   ├── conftest.py

│   ├── test\_http\_checks.py

│   ├── test\_link\_checks.py

│   ├── test\_forms\_checks.py

│   └── test\_ui\_checks.py

│

├── reports/

├── screenshots/

│

├── audit\_report\_template.md

├── bug\_report\_template.md

├── checklist.md

├── config.py

├── main.py

├── report\_writer.py

├── test\_agent.py

├── pytest.ini

├── requirements.txt

├── .gitignore

└── README.md

```





\## HTTP-проверка



Модуль `http\_checks.py` проверяет:



\- доступность URL;

\- HTTP status code;

\- время HTTP-ответа;

\- сетевые ошибки.



Базовая классификация времени ответа:



```text

< 1 сек      PASS

1–3 сек      WARN

> 3 сек      FAIL

```



Важно: это время HTTP-ответа сервера, а не полноценный frontend performance audit и не Core Web Vitals.





\## Проверка ссылок



Модуль `link\_checks.py`:



\- получает ссылки со страницы;

\- выбирает внутренние ссылки;

\- нормализует URL;

\- удаляет fragment;

\- приводит scheme и domain к нижнему регистру;

\- убирает лишний trailing slash;

\- сохраняет query parameters;

\- проверяет HTTP status code;

\- определяет битые ссылки.



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





\## Проверка форм



Модуль `forms\_checks.py` анализирует HTML-формы.



Для каждой формы определяется:



\- HTTP method;

\- action;

\- количество полей;

\- tag;

\- type;

\- name;

\- наличие `required`;

\- количество submit-кнопок.



Одинаковые формы группируются по:



\- method;

\- action;

\- набору полей.



Если одинаковая форма встречается в DOM несколько раз, сервис выводит её один раз и отдельно указывает количество экземпляров.



Пример:



```text

Форма #1

Экземпляров: 4

Method: GET

Action: https://filsnab.ru/catalog/

Количество полей в одном экземпляре: 2

Submit-кнопок в одном экземпляре: 1



\- input | type=text | name=q | required=False

\- input | type=hidden | name=type | required=False

```





\## Selenium UI-аудит



Модуль `ui\_checks.py` запускает Firefox в headless-режиме.



Проверяются:



\- загрузка страницы;

\- `title`;

\- наличие `title`;

\- наличие `h1`;

\- текст `h1`;

\- наличие ссылок;

\- количество ссылок;

\- наличие кнопок;

\- количество кнопок.



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





\## Проверка изображений



Сервис анализирует элементы `<img>`.



Определяется:



\- общее количество изображений;

\- количество изображений с `alt`;

\- количество изображений без `alt`;

\- список `src` найденных изображений без `alt`.



Если найдено изображение без `alt`, UI status становится `WARN`.



Пример:



```text

Images count: 3

Images with alt: 2

Images without alt: 1

```





\## Audit Analyzer



`agent/analyzer.py` получает структурированный результат QA Audit Service и выделяет подтверждённые технические проблемы.



Например:



```text

404

→ confirmed issue

```



Потенциально спорные находки не добавляются в confirmed issues автоматически.





\## Issue Prioritizer



`agent/prioritizer.py` назначает найденным проблемам приоритет:



```text

CRITICAL

HIGH

MEDIUM

LOW

```



Пример:



```text

16 broken internal links

→ HIGH

```





\## Manual Check Generator



`agent/manual\_checks.py` формирует отдельный список ситуаций, которые требуют контекста требований или ручной QA-проверки.



Например:



```text

Forms

→ проверить необходимость required



SEO/UI

→ проверить требования к H1



Accessibility

→ проверить назначение изображения без alt

```





\## QA Summary Generator



`agent/summary\_generator.py` формирует краткое итоговое QA-заключение.



Пример:



```text

Подтверждённых проблем: 1

CRITICAL: 0

HIGH: 1

MEDIUM: 0

LOW: 0

Требуют ручной проверки: 3



Итог: обнаружены серьёзные проблемы.

Рекомендуется в первую очередь устранить HIGH-дефекты

и затем выполнить повторный аудит.

```





\## Bug Report Generator



`agent/bug\_report\_generator.py` автоматически создаёт черновики bug reports для подтверждённых проблем.



Структура:



```text

ID

Title

Category

Priority

Preconditions

Steps

Expected Result

Actual Result

Evidence

```



Пример:



```text

BUG-001 — Обнаружены битые внутренние ссылки



Category: Links

Priority: HIGH

```





\## AI QA Agent Report



После работы агента автоматически создаётся отдельный Markdown-файл:



```text

reports/agent\_YYYY-MM-DD\_HH-MM-SS.md

```



В него входят:



\- QA Summary;

\- Confirmed Issues;

\- Priority;

\- Evidence;

\- Manual Checks;

\- Bug Report Drafts.



Evidence для битых ссылок сохраняется в читаемом формате:



```text

broken\_links\_count: 16

broken\_links:

&#x20; - 404 | https://example.com/page1

&#x20; - 404 | https://example.com/page2

```





\## Автотесты



Проект содержит автоматические тесты для:



\- HTTP-проверок;

\- классификации времени ответа;

\- внутренних ссылок;

\- нормализации URL;

\- битых ссылок;

\- HTML-форм;

\- Selenium UI-проверок;

\- `title`;

\- `h1`;

\- ссылок;

\- кнопок;

\- изображений;

\- атрибутов `alt`.



Текущий полный набор:



```text

37 passed

```



После интеграции AI QA Agent существующий regression suite продолжает проходить:



```text

37 passed in 23.50s

```





\## Unit и integration tests



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



Результат:



```text

25 passed, 12 deselected

```



Запуск integration tests:



```bash

pytest -v -m integration

```



Результат:



```text

12 passed, 25 deselected

```



Запуск полного набора:



```bash

pytest -v

```





\## Оптимизация Selenium tests



Selenium UI-тесты используют общий browser fixture из `tests/conftest.py`.



Firefox запускается один раз на тестовую сессию и переиспользуется между UI-тестами.



До оптимизации UI-тесты выполнялись примерно:



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





\## Обработка Selenium ошибок



Если Selenium не может загрузить страницу, сервис не завершает весь аудит аварийно.



Обрабатываются:



\- `TimeoutException`;

\- `WebDriverException`;

\- другие непредвиденные ошибки.



При timeout возвращается структурированный результат:



```text

UI status: ERROR

Title:

Title exists: False

H1 exists: False

H1 text:

Error: Page load timeout

```





\## Screenshots



При UI-ошибке сервис автоматически сохраняет screenshot:



```text

screenshots/

```



Пример:



```text

screenshots/ui\_error\_2026-10-05\_00-33-46.png

```



Путь к screenshot добавляется в итоговый audit report.





\## Отчёты



После одного запуска создаются два типа Markdown-отчётов.



\### QA Audit Service



```text

reports/audit\_YYYY-MM-DD\_HH-MM-SS.md

```



Содержит технические результаты автоматического аудита.



\### AI QA Agent



```text

reports/agent\_YYYY-MM-DD\_HH-MM-SS.md

```



Содержит аналитический слой:



\- confirmed issues;

\- priorities;

\- manual checks;

\- QA summary;

\- bug report drafts;

\- evidence.





\## Запуск



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

https://filsnab.ru

```



После этого автоматически выполняется:



```text

QA Audit Service

↓

AI QA Agent

↓

два Markdown-отчёта

```





\## Установка



Клонировать репозиторий:



```bash

git clone https://github.com/dimadvorokovsky/qa-audit-service.git

```



Перейти в каталог:



```bash

cd qa-audit-service

```



Создать virtual environment:



```bash

python -m venv venv

```



Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Если PowerShell блокирует скрипт:



```powershell

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

```



После этого:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Windows CMD:



```bat

venv\\Scripts\\activate

```



Установить зависимости:



```bash

pip install -r requirements.txt

```





\## Ручное тестирование



Кроме автоматизированных проверок в репозитории находятся:



\- `checklist.md` — универсальный QA checklist;

\- `bug\_report\_template.md` — шаблон bug report;

\- `audit\_report\_template.md` — шаблон итогового аудита.



Checklist включает:



\- доступность;

\- навигацию;

\- формы;

\- кнопки;

\- контент;

\- responsive checks;

\- пользовательские сценарии;

\- negative scenarios;

\- UX;

\- финализацию QA-аудита.





\## Архитектурные решения



В проекте реализованы:



\- разделение технических проверок по модулям;

\- отдельный report writer;

\- обработка ошибок отдельных модулей;

\- structured results через dictionaries;

\- URL normalization;

\- reusable Selenium driver;

\- pytest fixtures;

\- unit/integration separation;

\- автоматическое сохранение evidence при UI-ошибке;

\- дедупликация одинаковых HTML-форм;

\- группировка битых ссылок по URL-веткам;

\- отдельный agent layer;

\- разделение confirmed issues и manual checks;

\- rule-based prioritization;

\- автоматическая генерация QA Summary;

\- автоматическая генерация bug report drafts;

\- отдельный Markdown-report для агента.





\## Real-world audit case: filsnab.ru



QA Audit Service был протестирован на реальном веб-сайте:



```text

https://filsnab.ru/

```



\### Результат технического аудита



```text

Status Code: 200 OK

Performance: PASS



Проверено внутренних ссылок: 20

Найдено битых ссылок: 16



Уникальных форм: 1

Экземпляров формы в DOM: 4



Title exists: True

H1 exists: False



Images count: 15

Images without alt: 1

```



Проблемные URL-ветки:



```text

/catalog/filtratsiya — 7 битых ссылок

/catalog/filtratsiyaa — 7 битых ссылок

/blogg — 1 битая ссылка

/catalog/gidravlika — 1 битая ссылка

```



По результатам реального аудита QA Audit Service был доработан:



\- добавлена дедупликация одинаковых форм;

\- добавлен подсчёт экземпляров формы в DOM;

\- добавлена группировка битых URL по проблемным веткам;

\- улучшена структура Markdown-отчёта;

\- улучшено отображение Evidence.



Материалы:



\[`examples/filsnab.ru/README.md`](examples/filsnab.ru/README.md)



\[`examples/filsnab.ru/audit.md`](examples/filsnab.ru/audit.md)





\## AI QA Agent — real-world case



После технического аудита `filsnab.ru` результаты были переданы AI QA Agent Core.



Результат:



```text

Confirmed Issues: 1

HIGH: 1

Manual Checks: 3

Bug Report Drafts: 1

```



\### Confirmed Issue



Подтверждённая проблема:



```text

16 внутренних ссылок возвращают HTTP 404

Priority: HIGH

```



Для каждой ссылки сохраняется Evidence:



```text

404 | URL

```



\### Manual Checks



Агент отдельно сформировал:



1\. Проверить необходимость обязательных полей формы.

2\. Проверить требования к H1 на конкретном типе страницы.

3\. Проверить необходимость alt для найденного изображения.



Эти находки не объявляются багами автоматически без дополнительного контекста.



\### Bug Report Draft



Для подтверждённой проблемы сформирован bug report draft с:



\- Preconditions;

\- Steps;

\- Expected Result;

\- Actual Result;

\- Evidence.



Материалы кейса:



\[`examples/ai-qa-agent/README.md`](examples/ai-qa-agent/README.md)



Готовый отчёт:



\[`examples/ai-qa-agent/agent\_report.md`](examples/ai-qa-agent/agent\_report.md)





\## Цель проекта



Цель проекта — создать не просто набор учебных автотестов, а самостоятельный QA-инструмент, который способен:



```text

найти технические проблемы

→ собрать evidence

→ структурировать результаты

→ отделить факты от спорных находок

→ определить приоритет

→ сформировать QA summary

→ подготовить bug report drafts

```



Проект демонстрирует практику работы с:



\- manual QA;

\- web testing;

\- API/HTTP;

\- HTML parsing;

\- Selenium;

\- Python;

\- pytest;

\- fixtures;

\- test architecture;

\- error handling;

\- QA reporting;

\- automated QA analysis;

\- Git/GitHub.





\## Roadmap



Дальнейшее развитие проекта:



\- LLM-слой для дополнительного анализа результатов;

\- генерация дополнительных exploratory/manual test ideas;

\- автоматическое создание bug reports в issue tracker;

\- GitHub Actions;

\- Allure report generation;

\- HTML reports;

\- PDF reports;

\- FastAPI interface;

\- история аудитов;

\- database;

\- Docker;

\- параллельная проверка ссылок;

\- дополнительные accessibility checks;

\- CI/CD;

\- запуск аудитов для реальных пользователей и клиентов.





\## Автор



\*\*Dmitry Dvorokovsky\*\*



Junior QA Engineer



GitHub:



https://github.com/dimadvorokovsky

