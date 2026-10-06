\# AI QA Agent — Real-world Case



\## Цель



Проверить работу AI QA Agent поверх существующего QA Audit Service на реальном веб-сайте и показать полный цикл обработки результатов автоматического аудита.



\## Проверяемый сайт



https://filsnab.ru/



\## Архитектура



```text

URL сайта

↓

QA Audit Service

↓

HTTP / Links / Forms / Selenium / Images

↓

структурированный результат аудита

↓

AI QA Agent

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

Markdown Agent Report

