from pydantic import BaseModel, ConfigDict, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserBase(BaseModel):
    name: str = ""
    role: str
    phone: PhoneNumber 

class UserCreate(UserBase):
    telegram_id: int

class UserUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    phone: PhoneNumber | None = None  
    
    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        if not any([self.name, self.role, self.phone]):
            raise ValueError('Хотя бы одно поле должно быть указано для обновления')
        return self


class UserResponse(UserBase):
    id: int
    telegram_id: int
    model_config = ConfigDict(from_attributes=True)