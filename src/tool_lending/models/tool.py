from dataclasses import dataclass

@dataclass
class Tool:
    id: int
    name: str
    category: str
    stock: int

    def __post_init__(self):
        if not self.name:
            raise ValueError("El nombre no puede estar vacío")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")