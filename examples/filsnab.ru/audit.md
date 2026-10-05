# QA Audit Report

## Общая информация

- URL: https://filsnab.ru
- Дата проверки: 05.10.2026 22:35:01
- Общий статус: **WARN**

## Основная проверка

- Status code: 200
- Response time: 0.187 sec
- Available: True
- Performance: PASS

## Проверка ссылок

- Проверено ссылок: 20
- Битых ссылок: 16
- Результат: **Найдены проблемные ссылки**

### Проблемные ветки

- /catalog/filtratsiya — 7 битых ссылок
- /catalog/filtratsiyaa — 7 битых ссылок
- /blogg — 1 битая ссылка
- /catalog/gidravlika — 1 битая ссылка

### Битые ссылки

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

## Проверка форм

- Уникальных форм: 1
- Всего экземпляров форм в DOM: 4
- Всего полей во всех экземплярах: 8
- Submit-кнопок во всех экземплярах: 4

### Форма #1

- Экземпляров: 4
- Method: GET
- Action: https://filsnab.ru/catalog/
- Количество полей в одном экземпляре: 2
- Submit-кнопок в одном экземпляре: 1

#### Поля формы

- input | type=text | name=q | required=False
- input | type=hidden | name=type | required=False

## UI-проверка через Selenium

- UI status: WARN
- Title: ФИЛСНАБ - фильтры, РВД, шланги в сборе, фитинги, гидравлическое оборудование в Москве
- Title exists: True
- H1 exists: False
- H1 text: 
- Links exist: True
- Links count: 310
- Buttons exist: True
- Buttons count: 7

## Проверка изображений

- Images count: 15
- Images with alt: 14
- Images without alt: 1

### Изображения без alt

- https://partners.aspro.ru/upload/iblock/4bb/90_na_40_2_Montazhnaya_oblast_1.png


## Краткое заключение

Автоматические проверки завершены с предупреждениями. Рекомендуется изучить найденные проблемы подробнее.
