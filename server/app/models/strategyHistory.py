from pydantic import BaseModel
from datetime import datetime

# MongoDB에 저장될 히스토리 모델
class StrategyHistory(BaseModel):
    user_id: str
    meassage: str
    created_at: datetime
    