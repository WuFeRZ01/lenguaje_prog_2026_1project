from dataclasses import dataclass

@dataclass
class Member:
    id: int
    name: str

    def __post_init__(self):
        if not self.name:
            raise ValueError("El nombre no puede estar vacío")