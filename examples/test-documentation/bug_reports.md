\# Bug Reports — Web Application



\## BUG-001 — Внутренняя ссылка возвращает 404



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser

\- Connection: stable internet



\*\*Preconditions:\*\*

\- Главная страница сайта доступна.

\- На странице присутствует внутренняя ссылка.



\*\*Steps to Reproduce:\*\*

1\. Открыть главную страницу сайта.

2\. Найти ссылку на внутренний раздел.

3\. Нажать на ссылку.

4\. Дождаться загрузки страницы.



\*\*Actual Result:\*\*

Открывается страница с HTTP status code 404.



\*\*Expected Result:\*\*

Должна открываться существующая страница с ожидаемым контентом и успешным HTTP status code.



\*\*Evidence:\*\*

\- URL проблемной страницы;

\- HTTP status code;

\- screenshot страницы ошибки;

\- данные из DevTools Network.





\## BUG-002 — Форма отправляется с пустым обязательным полем



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Открыта страница с формой.

\- Форма содержит обязательное поле.



\*\*Steps to Reproduce:\*\*

1\. Открыть форму.

2\. Оставить обязательное поле пустым.

3\. Остальные поля заполнить валидными данными.

4\. Нажать кнопку отправки.



\*\*Actual Result:\*\*

Форма успешно отправляется без заполнения обязательного поля.



\*\*Expected Result:\*\*

Форма не должна отправляться.

Пользователь должен получить сообщение о необходимости заполнить обязательное поле.



\*\*Evidence:\*\*

\- screenshot формы;

\- request payload;

\- response сервера.





\## BUG-003 — Двойной клик создаёт дубликат заявки



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Открыта форма создания заявки.

\- Все обязательные поля заполнены валидными данными.



\*\*Steps to Reproduce:\*\*

1\. Заполнить форму валидными данными.

2\. Дважды быстро нажать кнопку отправки.

3\. Проверить созданные заявки.



\*\*Actual Result:\*\*

Создаются две одинаковые заявки.



\*\*Expected Result:\*\*

После первого нажатия должна создаваться только одна заявка.

Повторная отправка должна блокироваться.



\*\*Evidence:\*\*

\- screenshot;

\- два одинаковых request в Network;

\- идентификаторы созданных заявок.





\## BUG-004 — API принимает запрос без обязательного поля



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- Tool: Postman

\- API: REST

\- Content-Type: application/json



\*\*Preconditions:\*\*

\- Известен POST endpoint.

\- Известна валидная структура request body.



\*\*Steps to Reproduce:\*\*

1\. Сформировать валидный request body.

2\. Удалить обязательное поле.

3\. Отправить POST-запрос.

4\. Проверить response.



\*\*Actual Result:\*\*

Сервер принимает запрос и создаёт сущность без обязательного поля.



\*\*Expected Result:\*\*

Сервер должен отклонить запрос и вернуть error status code согласно API-контракту.



\*\*Evidence:\*\*

\- request;

\- response;

\- status code;

\- ID созданной сущности, если она была создана.





\## BUG-005 — API возвращает 500 при передаче невалидного типа данных



\*\*Severity:\*\* Critical  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- Tool: Postman

\- API: REST

\- Content-Type: application/json



\*\*Preconditions:\*\*

\- Endpoint принимает JSON body.

\- Одно из полей ожидает значение типа integer.



\*\*Steps to Reproduce:\*\*

1\. Сформировать валидный request body.

2\. В поле типа integer передать строковое значение.

3\. Отправить запрос.

4\. Проверить response.



\*\*Actual Result:\*\*

API возвращает HTTP 500 Internal Server Error.



\*\*Expected Result:\*\*

API должен валидировать входные данные и вернуть клиентскую ошибку согласно контракту, например 400 Bad Request.



\*\*Evidence:\*\*

\- request body;

\- response body;

\- HTTP status code.





\## BUG-006 — В API response отображается stack trace



\*\*Severity:\*\* Critical  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- Tool: Postman

\- API: REST



\*\*Preconditions:\*\*

\- Есть возможность вызвать ошибочный запрос.



\*\*Steps to Reproduce:\*\*

1\. Отправить запрос с невалидными параметрами.

2\. Получить ответ сервера.

3\. Проверить response body.



\*\*Actual Result:\*\*

В response body отображается внутренний stack trace приложения.



\*\*Expected Result:\*\*

Пользователь API должен получать безопасное и понятное сообщение об ошибке без внутренних технических деталей.



\*\*Evidence:\*\*

\- response body;

\- HTTP status code.





\## BUG-007 — Защищённый endpoint доступен без авторизации



\*\*Severity:\*\* Critical  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- Tool: Postman

\- API: REST



\*\*Preconditions:\*\*

\- Endpoint должен быть доступен только авторизованному пользователю.



\*\*Steps to Reproduce:\*\*

1\. Не передавать Authorization header.

2\. Отправить запрос к защищённому endpoint.

3\. Проверить response.



\*\*Actual Result:\*\*

Сервер возвращает защищённые данные без авторизации.



\*\*Expected Result:\*\*

Сервер должен отклонить запрос и вернуть ошибку авторизации согласно API-контракту.



\*\*Evidence:\*\*

\- request headers;

\- response body;

\- HTTP status code.





\## BUG-008 — Некорректный email принимается формой



\*\*Severity:\*\* Minor  

\*\*Priority:\*\* Medium



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Открыта форма с полем Email.



\*\*Steps to Reproduce:\*\*

1\. Ввести в поле Email значение `test`.

2\. Заполнить остальные обязательные поля.

3\. Нажать кнопку отправки.



\*\*Actual Result:\*\*

Форма принимает невалидный email и отправляется.



\*\*Expected Result:\*\*

Должно отображаться сообщение о невалидном формате email.

Форма не должна отправляться до исправления значения.



\*\*Evidence:\*\*

\- screenshot;

\- request payload.





\## BUG-009 — На странице появляется горизонтальный скролл на мобильном разрешении



\*\*Severity:\*\* Minor  

\*\*Priority:\*\* Medium



\*\*Environment:\*\*

\- Browser: Chrome DevTools Device Toolbar

\- Viewport: 375 × 812 px



\*\*Preconditions:\*\*

\- Страница открыта на мобильном viewport.



\*\*Steps to Reproduce:\*\*

1\. Открыть DevTools.

2\. Включить Device Toolbar.

3\. Установить viewport 375 × 812 px.

4\. Открыть проверяемую страницу.

5\. Прокрутить страницу по горизонтали.



\*\*Actual Result:\*\*

Страница прокручивается по горизонтали.

Часть элементов выходит за границы viewport.



\*\*Expected Result:\*\*

Контент должен полностью помещаться по ширине мобильного экрана без нежелательного горизонтального скролла.



\*\*Evidence:\*\*

\- screenshot;

\- viewport size;

\- DOM-элемент, выходящий за границы.





\## BUG-010 — Ошибка API не отображается пользователю



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Пользователь выполняет действие, которое отправляет запрос в backend.

\- Backend возвращает ошибку.



\*\*Steps to Reproduce:\*\*

1\. Открыть страницу.

2\. Выполнить действие, вызывающее API request.

3\. Получить error response от сервера.

4\. Проверить интерфейс.



\*\*Actual Result:\*\*

Пользователь не получает сообщения об ошибке.

Интерфейс остаётся в состоянии загрузки или выглядит как успешно завершённый сценарий.



\*\*Expected Result:\*\*

Пользователь должен получить понятное сообщение о том, что операция не выполнена.

Интерфейс должен выйти из состояния загрузки.



\*\*Evidence:\*\*

\- screenshot;

\- request/response из Network;

\- HTTP status code.





\## BUG-011 — После исправления ошибки сообщение валидации не исчезает



\*\*Severity:\*\* Minor  

\*\*Priority:\*\* Medium



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Открыта форма с клиентской валидацией.



\*\*Steps to Reproduce:\*\*

1\. Ввести невалидное значение.

2\. Вызвать валидацию.

3\. Убедиться, что отображается сообщение об ошибке.

4\. Исправить значение на валидное.



\*\*Actual Result:\*\*

Сообщение об ошибке продолжает отображаться после исправления значения.



\*\*Expected Result:\*\*

После ввода валидного значения сообщение об ошибке должно исчезнуть.



\*\*Evidence:\*\*

\- screenshot до исправления;

\- screenshot после исправления.





\## BUG-012 — Приложение выполняет дублирующиеся API-запросы



\*\*Severity:\*\* Major  

\*\*Priority:\*\* Medium



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: Chrome DevTools



\*\*Preconditions:\*\*

\- Открыта страница приложения.

\- Вкладка Network очищена.



\*\*Steps to Reproduce:\*\*

1\. Открыть DevTools.

2\. Перейти во вкладку Network.

3\. Выполнить одно пользовательское действие.

4\. Проанализировать список запросов.



\*\*Actual Result:\*\*

Одно действие пользователя вызывает несколько одинаковых API-запросов без функциональной необходимости.



\*\*Expected Result:\*\*

Одно действие должно инициировать необходимое количество запросов согласно архитектуре приложения без необоснованного дублирования.



\*\*Evidence:\*\*

\- screenshot Network;

\- URL запросов;

\- method;

\- payload;

\- timestamps.





\## BUG-013 — Основная страница не восстанавливается после refresh



\*\*Severity:\*\* Major  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: актуальная версия Chrome / Yandex Browser



\*\*Preconditions:\*\*

\- Пользователь находится на внутренней странице приложения.



\*\*Steps to Reproduce:\*\*

1\. Перейти на внутреннюю страницу.

2\. Обновить страницу через браузер.



\*\*Actual Result:\*\*

После refresh отображается 404 либо пользователь неожиданно перенаправляется на главную страницу.



\*\*Expected Result:\*\*

После обновления должна открываться та же страница либо происходить ожидаемое восстановление состояния согласно требованиям.



\*\*Evidence:\*\*

\- URL;

\- screenshot;

\- HTTP status code;

\- Network log.





\## BUG-014 — Критическая JavaScript-ошибка ломает основной пользовательский сценарий



\*\*Severity:\*\* Critical  

\*\*Priority:\*\* High



\*\*Environment:\*\*

\- OS: Windows 10/11

\- Browser: Chrome DevTools



\*\*Preconditions:\*\*

\- Страница приложения открыта.



\*\*Steps to Reproduce:\*\*

1\. Открыть DevTools.

2\. Перейти во вкладку Console.

3\. Выполнить основной пользовательский сценарий.

4\. Зафиксировать ошибку.



\*\*Actual Result:\*\*

В Console появляется JavaScript error, после которого пользователь не может продолжить основной сценарий.



\*\*Expected Result:\*\*

Критические JavaScript errors отсутствуют.

Основной сценарий выполняется полностью.



\*\*Evidence:\*\*

\- Console error;

\- screenshot;

\- шаг сценария, на котором произошла ошибка.

