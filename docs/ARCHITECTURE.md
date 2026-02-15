# Архитектура проекта BioPotential

**Версия:** 1.0  
**Дата:** 14.02.2026

---

## 1. Общая структура репозитория (monorepo)

```
BioPotential/
├── README.md
├── Makefile                    # Команды: build, dev, test, migrate
├── docker-compose.yml          # Сборка и запуск всех сервисов
├── .env.example
│
├── docs/                       # Документация (не код)
│   ├── dizdoc.md               # Техническое задание
│   ├── ARCHITECTURE.md         # Этот файл
│   └── api/                    # OpenAPI/Swagger (опционально)
│
├── backend/                    # Python-бэкенд (FastAPI)
│   ├── pyproject.toml / requirements.txt
│   ├── alembic/                # Миграции БД
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py           # Pydantic Settings из env
│   │   ├── deps.py             # Зависимости (DB session, auth)
│   │   │
│   │   ├── api/                # HTTP endpoints
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py   # Сводный роутер
│   │   │   │   ├── auth.py
│   │   │   │   ├── tasks.py
│   │   │   │   ├── users.py
│   │   │   │   ├── drivers.py
│   │   │   │   ├── vehicles.py
│   │   │   │   ├── journal.py
│   │   │   │   └── files.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── core/               # Бизнес-логика
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Telegram auth, роли
│   │   │   ├── tasks.py
│   │   │   ├── journal.py
│   │   │   └── notifications.py
│   │   │
│   │   ├── services/           # Слой сервисов (оркестрация)
│   │   │   ├── __init__.py
│   │   │   ├── task_service.py
│   │   │   ├── assignment_service.py  # Вызов C++ ядра
│   │   │   ├── journal_service.py
│   │   │   └── notification_service.py
│   │   │
│   │   ├── models/             # SQLAlchemy/Tortoise модели
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── driver.py
│   │   │   ├── vehicle.py
│   │   │   ├── journal_entry.py
│   │   │   └── task_history.py
│   │   │
│   │   ├── schemas/            # Pydantic (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── task.py
│   │   │   ├── user.py
│   │   │   └── ...
│   │   │
│   │   ├── db/                 # Работа с БД
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   └── migrations/     # или alembic в корне backend
│   │   │
│   │   ├── integrations/       # Внешние системы
│   │   │   ├── __init__.py
│   │   │   ├── telegram.py     # Bot API
│   │   │   ├── core_api.py     # Клиент к C++ ядру (REST/gRPC)
│   │   │   └── storage.py      # MinIO или локальные файлы
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logging.py
│   │       └── permissions.py
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_tasks.py
│       └── ...
│
├── core/                       # C++ ядро (алгоритмы подбора)
│   ├── CMakeLists.txt
│   ├── README.md
│   ├── include/
│   │   ├── core/
│   │   │   ├── queue_manager.hpp
│   │   │   ├── assignment_algorithm.hpp
│   │   │   └── types.hpp
│   │   └── api/                # REST/gRPC сервер
│   │       └── server.hpp
│   ├── src/
│   │   ├── queue_manager.cpp
│   │   ├── assignment_algorithm.cpp
│   │   └── api/
│   │       └── server.cpp
│   ├── tests/
│   └── Dockerfile
│
├── frontend/                   # Telegram Web App
│   ├── package.json
│   ├── vite.config.ts / next.config.js  # выбор фреймворка
│   ├── tsconfig.json
│   ├── public/
│   ├── src/
│   │   ├── app/                # если Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── tasks/
│   │   │   ├── task/[id]/
│   │   │   ├── fleet/
│   │   │   ├── journal/
│   │   │   └── profile/
│   │   │
│   │   ├── components/
│   │   │   ├── ui/             # Кнопки, инпуты, карточки
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskDetail.tsx
│   │   │   ├── FileViewer.tsx  # PDF-просмотрщик
│   │   │   ├── FleetStatus.tsx
│   │   │   └── RoleGuard.tsx   # Скрытие UI по ролям
│   │   │
│   │   ├── hooks/
│   │   │   ├── useTelegram.ts
│   │   │   ├── useAuth.ts
│   │   │   └── useTasks.ts
│   │   │
│   │   ├── api/                # HTTP-клиент к backend
│   │   │   ├── client.ts
│   │   │   ├── tasks.ts
│   │   │   ├── auth.ts
│   │   │   └── ...
│   │   │
│   │   ├── stores/             # Состояние (zustand/jotai или context)
│   │   │   └── auth.ts
│   │   │
│   │   ├── types/
│   │   │   └── index.ts
│   │   │
│   │   └── lib/
│   │       └── utils.ts
│   │
│   └── Dockerfile
│
├── infrastructure/             # DevOps
│   ├── nginx/
│   │   └── nginx.conf
│   └── k8s/                    # опционально
│
└── projects/                   # НЕ использовать — из pet-project rules
    └── .gitkeep
```

---

## 2. Назначение слоёв (backend)

| Слой | Папка | Ответственность |
|------|-------|-----------------|
| **API** | `api/v1/` | Маршрутизация, валидация входных данных, вызов сервисов |
| **Core** | `core/` | Бизнес-правила, валидация прав, доменная логика |
| **Services** | `services/` | Оркестрация: вызов core, БД, C++, Telegram |
| **Models** | `models/` | SQLAlchemy-модели, связи, индексы |
| **Schemas** | `schemas/` | Pydantic: сериализация, валидация запросов/ответов |
| **Integrations** | `integrations/` | Внешние API (Telegram, C++ core, storage) |

**Поток запроса:** `API` → `Service` → `Core` + `Model` + `Integration`

---

## 3. Именование

- **Файлы:** snake_case (`task_service.py`, `assignment_algorithm.cpp`)
- **Классы:** PascalCase (`TaskService`, `AssignmentAlgorithm`)
- **Функции/методы:** snake_case (`create_task`, `get_available_drivers`)
- **Константы:** UPPER_SNAKE (`MAX_FILE_SIZE`)
- **API endpoints:** kebab-case (`/api/v1/tasks`, `/api/v1/journal-entries`)

---

## 4. Взаимодействие компонентов

```
┌─────────────────┐     HTTPS      ┌─────────────────┐
│  Telegram Web   │ ──────────────►│  Python Backend │
│  App (frontend) │                │  (FastAPI)      │
└─────────────────┘                └────────┬────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
            ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
            │  PostgreSQL  │       │  C++ Core    │       │  Telegram    │
            │              │       │  (REST/gRPC) │       │  Bot API     │
            └──────────────┘       └──────────────┘       └──────────────┘
                    │                       │
                    │                       ▼
                    │               ┌──────────────┐
                    └──────────────►│  MinIO /     │
                                    │  локальные   │
                                    │  файлы       │
                                    └──────────────┘
```

---

## 5. Ключевые принципы

1. **Разделение по модулям** — задачи, журнал, водители, ТС живут в своих API/core/services.
2. **Слой интеграций отдельно** — смена C++ на другой протокол не трогает services.
3. **Роли в core/auth** — проверка прав в одном месте, переиспользование.
4. **Миграции в alembic** — версионирование схемы БД.
5. **Тесты рядом с кодом** — `backend/tests/` зеркалирует структуру `app/`.

---

## 6. Рекомендуемый порядок реализации

1. **Backend: каркас** — `main.py`, `config`, `deps`, модели, alembic.
2. **Auth** — Telegram Web App initData, маппинг telegram_id → роль.
3. **CRUD задач** — создание, список, фильтрация, статусы.
4. **C++ core** — заглушка REST API, затем алгоритм подбора.
5. **Integrations** — вызов core, Telegram notifications, storage.
6. **Frontend** — страницы задач, детали, PDF, роли.
7. **Журнал, автопарк, наблюдатель.**
