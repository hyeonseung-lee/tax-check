from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from app.models.user import UserCreate
from app.db.database import users_collection, db
from datetime import datetime

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해시화 함수
async def hash_pwd(pwd: str) -> str:
    return pwd_context.hash(pwd)

# # 사용자 로그인 API
# @router.post("/login")
# async def login_user(user: UserCreate):
#     # 사용자가 존재하는지 확인
#     existing_user = await users_collection.find_one({"username": user.username})
#     if not existing_user:
#         raise HTTPException(status_code=400, detail="User not found")

#     # 저장된 해시된 비밀번호와 입력한 비밀번호 비교
#     if not pwd_context.verify(user.pwd, existing_user["hashed_pwd"]):
#         raise HTTPException(status_code=400, detail="Incorrect password")

#     return {"message": "User logged in successfully"}

# 사용자 로그인 API
@router.post("/login")
async def login_user():
    return {"message": "User logged in successfully"}

# 사용자 등록 API
@router.post("/register")
async def register_user(user: UserCreate):
    if "users" not in await db.list_collection_names():
        await db.create_collection("users")  # 컬렉션이 없으면 생성

    # 이미 존재하는 사용자 확인
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
       
    # 비밀번호 해시화
    hashed_pwd = await hashed_pwd(user.pwd)

    # 새 사용자 정보 MongoDB에 저장
    new_user = {
        "username": user.username,
        "hashed_pwd": hashed_pwd,
        "created_at": datetime.utcnow()
    }
    await users_collection.insert_one(new_user)

    return {"message": "User registered successfully"}

