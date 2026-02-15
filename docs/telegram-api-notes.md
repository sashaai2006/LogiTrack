# Заметки по Telegram Bot API для BioPotential

**Источники:** [Bot API](https://core.telegram.org/bots/api), [Web Apps](https://core.telegram.org/bots/webapps)

---

## 1. Запросы к API

- **Base URL:** `https://api.telegram.org/bot<TOKEN>/<METHOD>`
- **Методы:** GET и POST
- **Формат параметров:** `application/json`, `application/x-www-form-urlencoded`, `multipart/form-data`, query string
- **Кодировка:** UTF-8
- **Ответ:** `{ "ok": true, "result": {...} }` или `{ "ok": false, "description": "...", "error_code": ... }`

---

## 2. Авторизация в Web App (initData)

Mini App получает данные пользователя в `window.Telegram.WebApp`:

| Поле | Описание |
|------|----------|
| **initData** | Сырая строка для проверки на сервере. **Обязательно проверять на бэкенде.** |
| **initDataUnsafe** | Распарсенные данные. **На сервере не доверять.** |

**initDataUnsafe** содержит, в частности:
- `user` — id, first_name, last_name, username, language_code
- `auth_date` — unix timestamp
- `hash` — подпись для проверки

**Проверка на бэкенде:**
1. Берётся строка `initData`
2. Подпись проверяется через HMAC-SHA256 с ключом `WebAppData` (секрет из bot token)
3. Проверяется `auth_date` (не старше N минут)
4. Извлекается `user.id` (telegram_id) для привязки к роли

Telegram предлагает библиотеки для проверки: `@tma.js/init-data-node` (Node.js), `init-data-golang` (Go). Для Python подойдёт ручная проверка по [документации](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app).

**Схема:** фронт отправляет `initData` в заголовке `Authorization: tma <initData>` или в теле запроса.

---

## 3. Отправка уведомлений (sendMessage)

**Метод:** `sendMessage`

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| chat_id | Integer/String | да | telegram_id пользователя или ID чата |
| text | String | да | Текст сообщения (до 4096 символов) |
| parse_mode | String | нет | `"HTML"` или `"Markdown"` |
| disable_web_page_preview | Boolean | нет | Убрать превью ссылок |

**Пример запроса:**
```http
POST https://api.telegram.org/bot<TOKEN>/sendMessage
Content-Type: application/json

{
  "chat_id": 123456789,
  "text": "Новая задача #T-001: Доставить груз. Статус: В работе."
}
```

Чтобы отправлять сообщения пользователю, нужен его `chat_id`. В личных чатах `chat_id` = `telegram_id`. Пользователь должен хотя бы раз начать диалог с ботом (например, нажав Start или открыв Web App).

---

## 4. Получение обновлений (webhook vs polling)

**Webhook (для продакшена):**
- `setWebhook` — указать URL для POST-запросов с обновлениями
- Порты: 443, 80, 88, 8443
- Telegram шлёт JSON с `Update` при новых сообщениях и т.п.

**Polling (для разработки):**
- `getUpdates` — long polling за обновлениями
- С webhook не совместимо

Для BioPotential: уведомления шлёт backend через `sendMessage`, webhook можно использовать, если нужны команды/кнопки в чате. Для MVP достаточно `sendMessage` по сохранённому `telegram_id`.

---

## 5. Web App — способы запуска

| Способ | Описание |
|--------|----------|
| Menu Button | Кнопка в чате с ботом (BotFather → Menu Button) |
| Main Mini App | Кнопка "Launch app" в профиле бота |
| Inline Button | Кнопка `web_app` в сообщении |
| Direct Link | `https://t.me/botusername?startapp` или `https://t.me/botusername/appname` |

Рекомендуется Main Mini App или Menu Button для быстрого входа.

---

## 6. Скрипт Web App

Подключать до остальных скриптов:
```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

Доступ: `window.Telegram.WebApp`

---

## 7. Нужно для BioPotential

1. **Auth:** валидация `initData` на бэкенде, извлечение `user.id` → проверка роли в БД.
2. **Notifications:** `sendMessage` с `chat_id = telegram_id` (пользователь должен начать диалог с ботом).
3. **Хранение:** в модели User поле `telegram_id` — для отправки уведомлений.
4. **Bot Token:** хранить в env (`TELEGRAM_BOT_TOKEN`), не коммитить.
