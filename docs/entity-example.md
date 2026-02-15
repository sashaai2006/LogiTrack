# Паттерн сущности (пример: User)

Для каждой сущности создаём **4 слоя** в таком порядке:

---

## 1. Model (models/user.py) — уже есть

SQLAlchemy-модель — слой данных. Обычно создаётся первым.

---

## 2. Schema (schemas/user.py) — Pydantic

Схемы для валидации запросов и сериализации ответов.

**Правила:**
- `*Create` — тело POST (создание)
- `*Update` — тело PATCH (частичное обновление), все поля optional
- `*Response` / `*Read` — ответ API (без чувствительных данных)
- Базовый класс с общими полями, остальные наследуют

```python
# schemas/user.py
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    full_name: str = ""
    role: str  # manager, dispatcher, viewer
    contacts: str | None = None

class UserCreate(UserBase):
    telegram_id: int

class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None
    contacts: str | None = None

class UserResponse(UserBase):
    id: int
    telegram_id: int
    model_config = ConfigDict(from_attributes=True)
```

---

## 3. API Router (api/v1/users.py)

Эндпоинты. Логика — только вызов сервиса/репозитория.

```python
# api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    data = body.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user
```

---

## 4. Подключение

**api/v1/router.py** — собираем роутеры:
```python
from fastapi import APIRouter
from app.api.v1 import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
# или если prefix уже в router: api_router.include_router(users.router)
```

**main.py** — подключаем API:
```python
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
```

---

## Порядок для новой сущности (например, Driver)

1. `models/driver.py` — модель
2. `schemas/driver.py` — Create, Update, Response
3. `api/v1/drivers.py` — router с CRUD
4. Добавить в `api/v1/router.py`: `api_router.include_router(drivers.router)`
