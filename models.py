from pydantic import BaseModel, Field, field_validator
from datetime import date


class Expense(BaseModel):
    amount: float = Field(gt=0)
    category: str
    description: str | None = None
    date: date

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if not value.strip():
            raise ValueError("Category cannot be empty")

        return value.strip()

    @field_validator("date")
    @classmethod
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("Expense date cannot be in the future")

        return value