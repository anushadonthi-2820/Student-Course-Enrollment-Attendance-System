from dataclasses import dataclass


@dataclass
class Course:
    id: int | None
    name: str
    code: str
