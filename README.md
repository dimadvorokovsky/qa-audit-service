# QA Audit Service + QA Agent

Python-сервис для автоматизированного технического и UI-аудита веб-сайтов с дополнительным QA Agent.

Проект сочетает:

- HTTP-проверки;
- анализ внутренних ссылок;
- поиск битых ссылок;
- анализ HTML-форм;
- Selenium UI-проверки;
- проверку `title`;
- проверку H1;
- анализ изображений и `alt`;
- автоматическое формирование Markdown-отчётов;
- детерминированный QA Agent;
- приоритизацию найденных проблем;
- формирование manual checks;
- автоматические bug report drafts;
- дополнительный LLM-слой для интерпретации результатов.

---

## Current Status

На текущем этапе реализованы:

- QA Audit Service — готов;
- deterministic QA Agent — готов;
- LLM integration layer — готов;
- OpenAI provider — подключается опционально;
- fallback без API-ключа — реализован;
- unit-тесты LLM-слоя — реализованы;
- обработка ошибок Selenium — реализована;
- Markdown-отчёты — реализованы;
- real-world case study — реализован.

Текущий результат тестов:

```text
41 passed
```

LLM-провайдер не является обязательным для работы проекта.

Без API credentials сервис продолжает выполнять полный детерминированный аудит.

---

# Что делает проект

Сервис получает URL сайта и автоматически выполняет несколько групп проверок.

Общий процесс:

```text
URL
↓
QA Audit Service
↓
HTTP checks
Links checks
Forms checks
Selenium UI checks
Images checks
↓
Structured audit result
↓
Deterministic QA Agent
↓
Confirmed Issues
Manual Checks
QA Summary
Bug Report Drafts
↓
Optional LLM Analysis
↓
Markdown Report
```

---

# Архитектурный принцип

В проекте специально разделены:

```text
FACTS
```

и:

```text
AI INTERPRETATION
```

Фактические результаты формируются детерминированными проверками.

LLM не является источником технических фактов.

Он не должен:

- изменять HTTP status codes;
- изменять найденные URL;
- самостоятельно объявлять manual check подтверждённым дефектом;
- удалять confirmed issues;
- изменять evidence;
- утверждать, что дефект воспроизведён, если это не подтверждено автоматическими проверками.

LLM используется только как дополнительный аналитический слой.

---

# Основные возможности QA Audit Service

## HTTP

Проверяется:

- доступность URL;
- HTTP status code;
- response time;
- performance status.

Пример:

```text
Status code: 200
Response time: 0.19 sec
Available: True
Performance: PASS
```

---

## Internal Links

Сервис:

- получает внутренние ссылки страницы;
- нормализует URL;
- выполняет HTTP-проверки;
- определяет битые ссылки;
- сохраняет URL и status code.

Пример:

```text
BROKEN | 404 | https://example.com/catalog/test
```

---

## Forms

Сервис анализирует HTML-формы.

Для каждой формы фиксируются:

- method;
- action;
- поля;
- типы полей;
- `required`;
- submit buttons;
- количество одинаковых экземпляров формы в DOM.

Одинаковые формы дедуплицируются.

При этом сохраняется количество экземпляров:

```text
instances
```

Это позволяет отличить несколько одинаковых DOM-форм от нескольких различных форм.

---

## Selenium UI Checks

Используется Selenium + Firefox.

Проверяются:

- title;
- наличие H1;
- текст H1;
- ссылки;
- кнопки;
- изображения;
- alt-тексты.

При ошибках Selenium сервис не должен полностью прекращать аудит.

Вместо этого формируется:

```text
UI status: ERROR
```

и основная часть проекта продолжает работу.

---

## Screenshots

При некоторых Selenium-ошибках сервис может сохранить screenshot для последующего анализа.

Файлы сохраняются в:

```text
screenshots/
```

---

# Images

Сервис определяет:

- общее количество изображений;
- количество изображений с `alt`;
- количество изображений без `alt`;
- URL изображений без `alt`.

Важно:

отсутствие `alt` не всегда автоматически считается подтверждённым дефектом.

Назначение изображения может быть:

- контентным;
- декоративным.

Поэтому такие случаи QA Agent может отправлять в manual checks.

---

# Deterministic QA Agent

Поверх результатов автоматического аудита работает отдельное детерминированное ядро QA Agent.

Основные модули:

```text
agent/
├── analyzer.py
├── prioritizer.py
├── manual_checks.py
├── summary_generator.py
├── bug_report_generator.py
├── report_writer.py
└── llm_analyzer.py
```

---

## Analyzer

`AuditAnalyzer` преобразует результаты аудита в подтверждённые проблемы.

Пример подтверждённого дефекта:

```text
16 внутренних ссылок возвращают HTTP 404
```

Такой результат имеет конкретное evidence и может считаться подтверждённым.

---

## Prioritizer

`IssuePrioritizer` присваивает проблемам приоритеты:

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

---

## Manual Checks

`ManualCheckGenerator` отделяет факты, которые требуют дополнительного контекста.

Например:

```text
H1 отсутствует
```

не всегда автоматически является дефектом.

Поэтому агент создаёт manual check:

```text
Проверить требования к H1 на конкретном типе страницы
```

То же правило применяется к:

- `required` в формах;
- изображениям без `alt`;
- другим находкам, зависящим от требований.

---

# QA Summary

`QASummaryGenerator` формирует общий результат.

Пример:

```text
Подтверждённых проблем: 1
CRITICAL: 0
HIGH: 1
MEDIUM: 0
LOW: 0
Требуют ручной проверки: 3
```

---

# Bug Report Drafts

`BugReportGenerator` автоматически создаёт черновики баг-репортов.

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

Это именно draft, который QA Engineer может дополнительно проверить и отредактировать перед регистрацией дефекта.

---

# LLM Layer

В проект добавлен отдельный LLM-слой поверх детерминированного QA Agent.

Архитектура:

```text
QA Audit Service
↓
Deterministic QA Agent
↓
Confirmed Issues
Manual Checks
QA Summary
Bug Report Drafts
↓
Optional LLM Analysis
```

---

## Что делает LLM

LLM может:

- сформировать executive summary;
- дать risk assessment;
- предложить дополнительные manual checks;
- предложить улучшения bug report drafts;
- сформировать confidence notes.

---

## Что LLM не делает

LLM не может считаться источником фактических результатов аудита.

Подтверждёнными остаются только данные deterministic core.

Например:

```text
Confirmed Issues
```

формируются до вызова LLM и не заменяются AI-анализом.

---

# LLM Output

Ожидаемая структура:

```json
{
  "executive_summary": "string",
  "risk_assessment": "string",
  "additional_manual_checks": [
    {
      "title": "string",
      "reason": "string"
    }
  ],
  "bug_report_improvements": [
    {
      "issue": "string",
      "suggestion": "string"
    }
  ],
  "confidence_notes": [
    "string"
  ]
}
```

---

# Работа без API-ключа

LLM является опциональным.

Если API не настроен, проект продолжает работать.

Результат:

```text
LLM ANALYSIS

Status: unavailable
Reason: OPENAI_API_KEY or OPENAI_MODEL is not configured
```

При этом:

- HTTP checks работают;
- links checks работают;
- forms checks работают;
- Selenium checks работают;
- deterministic QA Agent работает;
- bug report drafts формируются;
- Markdown-отчёт создаётся.

---

# Настройка LLM

Для подключения OpenAI API используются переменные окружения.

Создать локальный файл:

```text
.env
```

Пример:

```text
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_model
```

`.env` не должен попадать в Git.

Он исключён через `.gitignore`.

API key нельзя хранить:

- в Python-коде;
- в README;
- в GitHub;
- в тестах.

---

# LLM Error Handling

Реализованы fallback-сценарии.

## API не настроен

Результат:

```text
status: unavailable
```

---

## API недоступен

Результат:

```text
status: error
```

Основной аудит при этом не прекращается.

---

## LLM вернул невалидный JSON

Результат:

```text
status: error
reason: LLM returned invalid JSON
```

---

# Тестирование LLM Layer

LLM-тесты не выполняют реальные платные API-запросы.

Используются mocks.

Покрыты сценарии:

- отсутствует API configuration;
- успешный JSON response;
- invalid JSON;
- API exception.

Файл:

```text
tests/test_llm_analyzer.py
```

---

# Tests

Запуск всей тестовой системы:

```bash
python -m pytest -q
```

Текущий результат:

```text
41 passed
```

В тестах проверяются как существующие функции QA Audit Service, так и новый LLM layer.

---

# Reports

Сервис создаёт два типа Markdown-отчётов.

## QA Audit Service

```text
reports/audit_YYYY-MM-DD_HH-MM-SS.md
```

---

## QA Agent

```text
reports/agent_YYYY-MM-DD_HH-MM-SS.md
```

Agent report содержит:

```text
Deterministic QA Summary
Confirmed Issues
Manual Checks
Bug Report Drafts
LLM Analysis
```

---

# Пример LLM fallback в отчёте

```markdown
## LLM Analysis

**Status:** unavailable

**Reason:** OPENAI_API_KEY or OPENAI_MODEL is not configured

Детерминированные результаты аудита остаются доступными выше.
```

Таким образом отчёт остаётся полезным даже без подключения AI provider.

---

# Real-world Audit Case

Для проверки сервиса использовался реальный сайт:

```text
https://filsnab.ru
```

Case study находится в:

```text
examples/filsnab.ru/
```

---

## Результаты аудита filsnab.ru

Основной URL:

```text
https://filsnab.ru
```

HTTP:

```text
200 OK
```

Performance:

```text
PASS
```

Во время проверки было найдено:

```text
20 внутренних ссылок
16 broken links
```

Все найденные broken links возвращали:

```text
HTTP 404
```

---

## Примеры найденных broken links

```text
https://filsnab.ru/blogg
https://filsnab.ru/catalog/filtratsiya
https://filsnab.ru/catalog/filtratsiya/gidravlicheskie-filtry
https://filsnab.ru/catalog/filtratsiya/maslyanye-filtry
https://filsnab.ru/catalog/filtratsiya/osushiteli-tormozov
https://filsnab.ru/catalog/filtratsiya/salonnye-filtry
https://filsnab.ru/catalog/filtratsiya/toplivnye-filtry
https://filsnab.ru/catalog/filtratsiya/vozdushnye-filtry
https://filsnab.ru/catalog/filtratsiyaa
https://filsnab.ru/catalog/gidravlika
```

---

## Forms

Найдена одна уникальная форма:

```text
Method: GET
Action: https://filsnab.ru/catalog/
Fields: 2
DOM instances: 4
```

Несмотря на наличие четырёх экземпляров в DOM, сервис определяет их как одну логически одинаковую форму.

---

## UI

Selenium-проверка:

```text
Title exists: True
H1 exists: False
```

Изображения:

```text
Images count: 15
Images with alt: 14
Images without alt: 1
```

Изображение без `alt`:

```text
https://partners.aspro.ru/upload/iblock/4bb/90_na_40_2_Montazhnaya_oblast_1.png
```

---

# QA Agent Case Study

Пример результата QA Agent находится в:

```text
examples/ai-qa-agent/
```

Для `filsnab.ru` deterministic core сформировал:

```text
Confirmed Issues: 1
Manual Checks: 3
Bug Report Drafts: 1
```

---

## Confirmed Issue

```text
[HIGH] Broken internal links
```

Evidence:

```text
16 URLs
HTTP 404
```

---

## Manual Checks

Сформированы проверки:

```text
1. Проверить необходимость обязательных полей формы
2. Проверить требования к H1
3. Проверить необходимость alt для изображения
```

Это демонстрирует принцип:

```text
автоматически найденный факт
≠
автоматически подтверждённый дефект
```

---

# Example Structure

```text
examples/
├── filsnab.ru/
│   ├── README.md
│   └── audit.md
│
├── ai-qa-agent/
│   ├── README.md
│   └── agent_report.md
│
└── test-documentation/
    ├── README.md
    ├── checklist.md
    ├── test_cases.md
    └── bug_reports.md
```

---

# Test Documentation Examples

В репозитории также есть отдельные примеры тестовой документации:

```text
examples/test-documentation/
```

Включены:

- checklist;
- test cases;
- bug reports.

Эти материалы используются как часть QA-портфолио.

---

# Project Structure

Пример основной структуры проекта:

```text
qa-audit-service/
│
├── agent/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── prioritizer.py
│   ├── manual_checks.py
│   ├── summary_generator.py
│   ├── bug_report_generator.py
│   ├── report_writer.py
│   └── llm_analyzer.py
│
├── checks/
│   ├── http_checks.py
│   ├── link_checks.py
│   ├── forms_checks.py
│   └── ui_checks.py
│
├── examples/
│   ├── filsnab.ru/
│   ├── ai-qa-agent/
│   └── test-documentation/
│
├── reports/
├── screenshots/
├── tests/
│   └── test_llm_analyzer.py
│
├── .gitignore
├── main.py
├── report_writer.py
├── requirements.txt
└── README.md
```

---

# Installation

Клонировать репозиторий:

```bash
git clone https://github.com/dimadvorokovsky/qa-audit-service.git
```

Перейти в папку:

```bash
cd qa-audit-service
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Установить зависимости:

```bash
python -m pip install -r requirements.txt
```

---

# Run

Запустить:

```bash
python main.py
```

Сервис запросит:

```text
Введите URL сайта:
```

Пример:

```text
https://filsnab.ru
```

---

# Technologies

Используются:

```text
Python
Requests
BeautifulSoup
Selenium
Firefox
pytest
OpenAI Python SDK
python-dotenv
Markdown
Git
GitHub
```

---

# Reliability

Проект разработан так, чтобы сбой отдельного дополнительного компонента по возможности не останавливал весь аудит.

Например:

```text
Selenium startup error
↓
UI status: ERROR
↓
остальные результаты продолжают обрабатываться
```

Аналогично:

```text
LLM unavailable
↓
Status: unavailable
↓
deterministic report remains available
```

---

# Security

API credentials не хранятся в репозитории.

`.gitignore` исключает:

```text
.env
```

Сгенерированные audit reports также не должны автоматически попадать в Git:

```text
reports/audit_*.md
reports/agent_*.md
```

В Git сохраняются только специально подготовленные portfolio examples.

---

# Current Limitations

Текущая версия имеет намеренно ограниченный scope.

Сервис не заменяет полноценное ручное тестирование.

Автоматические результаты необходимо интерпретировать с учётом:

- требований;
- бизнес-логики;
- назначения страницы;
- пользовательских сценариев;
- окружения.

LLM recommendations также являются вспомогательными и не заменяют подтверждённое evidence.

---

# Development Roadmap

Реализовано:

- HTTP audit;
- internal links audit;
- broken links detection;
- URL normalization;
- forms analysis;
- form deduplication;
- Selenium UI checks;
- H1/title checks;
- image alt analysis;
- screenshots on UI errors;
- Markdown reports;
- deterministic QA Agent;
- issue prioritization;
- manual checks;
- QA summary;
- bug report drafts;
- LLM integration layer;
- LLM fallback;
- mocked LLM unit tests;
- real-world case study.

Возможное дальнейшее развитие:

- подключение реального LLM provider для production use;
- расширение API checks;
- JavaScript console error analysis;
- Network request analysis;
- configurable audit rules;
- HTML report;
- CLI arguments;
- CI integration;
- более глубокие accessibility checks.

---

# Author

Dmitry Dvorokovsky

Junior QA Engineer

GitHub:

https://github.com/dimadvorokovsky