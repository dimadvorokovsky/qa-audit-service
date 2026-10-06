# AI QA Agent Report

**URL:** https://filsnab.ru

**Generated:** 2026-10-06 12:29:18

---

## QA Summary

```text
QA SUMMARY

Подтверждённых проблем: 1
CRITICAL: 0
HIGH: 1
MEDIUM: 0
LOW: 0
Требуют ручной проверки: 3

Итог: обнаружены серьёзные проблемы.
Рекомендуется в первую очередь устранить HIGH-дефекты и затем выполнить повторный аудит.

Основные проблемы:
- [HIGH] Обнаружены битые внутренние ссылки

Что проверить вручную:
- Проверить необходимость обязательных полей формы
- Проверить требования к H1 на конкретном типе страницы
- Проверить необходимость alt для найденных изображений
```

---

## Confirmed Issues

Всего: **1**

### 1. [HIGH] Обнаружены битые внутренние ссылки

**Category:** Links

**Description:** Во время аудита найдено битых ссылок: 16.

**Evidence:**

```text
broken_links_count: 16
broken_links:
  - 404 | https://filsnab.ru/blogg
  - 404 | https://filsnab.ru/catalog/filtratsiya
  - 404 | https://filsnab.ru/catalog/filtratsiya/gidravlicheskie-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/maslyanye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/osushiteli-tormozov
  - 404 | https://filsnab.ru/catalog/filtratsiya/salonnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/toplivnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/vozdushnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/gidravlicheskie-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/maslyanye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/osushiteli-tormozov
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/salonnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/toplivnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/vozdushnye-filtry
  - 404 | https://filsnab.ru/catalog/gidravlika
```

---

## Manual Checks

Требуют ручной проверки: **3**

### 1. Проверить необходимость обязательных полей формы

**Category:** Forms

**Reason:** В форме не обнаружено полей с атрибутом required. Это не обязательно является дефектом и требует проверки бизнес-логики.

**Context:**

```text
method: GET
action: https://filsnab.ru/catalog/
instances: 4
fields_count: 2
```

### 2. Проверить требования к H1 на конкретном типе страницы

**Category:** SEO/UI

**Reason:** H1 отсутствует. Автоматическая проверка фиксирует факт, но необходимость H1 зависит от требований и структуры страницы.

**Context:**

```text
h1_exists: False
```

### 3. Проверить необходимость alt для найденных изображений

**Category:** Accessibility

**Reason:** Обнаружены изображения без атрибута alt. Это может быть проблемой доступности, но итоговая оценка зависит от назначения изображения: контентное оно или декоративное.

**Context:**

```text
images_without_alt_count: 1
images:
  - https://partners.aspro.ru/upload/iblock/4bb/90_na_40_2_Montazhnaya_oblast_1.png
```

---

## Bug Report Drafts

Создано черновиков: **1**

### BUG-001 — Обнаружены битые внутренние ссылки

**Category:** Links

**Priority:** HIGH

#### Preconditions

- Проверяемый сайт доступен.
- Главная страница успешно загружена.

#### Steps

1. Открыть проверяемый сайт.
2. Получить внутренние ссылки страницы.
3. Последовательно выполнить HTTP-проверку ссылок.
4. Зафиксировать ссылки с ошибочными HTTP status codes.

#### Expected Result

Внутренние ссылки должны вести на доступные страницы и не возвращать ошибочные HTTP status codes.

#### Actual Result

Обнаружено битых внутренних ссылок: 16.

#### Evidence

```text
broken_links_count: 16
broken_links:
  - 404 | https://filsnab.ru/blogg
  - 404 | https://filsnab.ru/catalog/filtratsiya
  - 404 | https://filsnab.ru/catalog/filtratsiya/gidravlicheskie-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/maslyanye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/osushiteli-tormozov
  - 404 | https://filsnab.ru/catalog/filtratsiya/salonnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/toplivnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiya/vozdushnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/gidravlicheskie-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/maslyanye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/osushiteli-tormozov
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/salonnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/toplivnye-filtry
  - 404 | https://filsnab.ru/catalog/filtratsiyaa/vozdushnye-filtry
  - 404 | https://filsnab.ru/catalog/gidravlika
```

---
