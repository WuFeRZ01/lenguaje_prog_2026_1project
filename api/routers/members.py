from fastapi import APIRouter
from api.services.member_service import get_members, create_member
from schemas.member_schema import MemberCreate

router = APIRouter(prefix="/members")

@router.get("/")
def list_members():
    return get_members()

@router.post("/")
def add_member(member: MemberCreate):
    return create_member(member.dict())