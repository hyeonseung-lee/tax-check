from pydantic import BaseModel
from datetime import datetime

# 사용자 생성 시 사용되는 Pydantic 모델
class UserCreate(BaseModel):
    username: str
    pwd: str

# MongoDB에 저장될 사용자 모델 (이 예시는 추가적으로 필요할 경우 사용할 수 있습니다)
class UserInDB(BaseModel):
    username: str
    hashed_pwd: str
    created_at: datetime
