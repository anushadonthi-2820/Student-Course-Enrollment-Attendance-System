from dataclasses import dataclass


@dataclass
class Student:
    id: int | None
    name: str
    email: str | None = None
    phone: str | None = None
    created_at: str | None = None
