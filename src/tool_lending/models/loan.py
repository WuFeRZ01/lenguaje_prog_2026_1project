from dataclasses import dataclass

@dataclass
class Loan:
    id: int
    member_id: int
    tool_id: int
    active: bool

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("ID inválido")