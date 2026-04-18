# Smart Bracelet Monitor (Web + Telegram)

Система мониторинга пульса с автоматическим уведомлением о критических состояниях.

## Функционал
* **Real-time Dashboard:** Визуализация данных в браузере через WebSockets/REST.
* **Alert System:** Автоматическая отправка уведомлений в Telegram при пульсе > 100 BPM.
* **Analytics:** Расчет среднего пульса и отслеживание истории за час.

## Технологии (Skills)
* **Backend:** Python (Flask). Проектирование REST API и работа с JSON.
* **Concurrency:** Использование `threading` для параллельного запуска сервера и бота.
* **Async:** Асинхронная логика бота на `asyncio`.
* **Frontend:** Динамические графики на **Chart.js** и JavaScript.
* **Architecture:** Принципы Event-driven (событие -> уведомление).

## Запуск
1. **Установка:** `pip install -r requirements.txt`
2. **Старт:** `python run_all.py`
* Бот: Начинает работу автоматически после запуска скрипта.

---
Badalov Shirinshoh
