from pydantic import BaseModel

class MemberCreate(BaseModel):
    name: str