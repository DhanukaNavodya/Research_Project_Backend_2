from pydantic import BaseModel
from datetime import datetime

class MoodCheckin(BaseModel):
    child_id: int
    mood: str
    note: str | None = None

    class Config:
        from_attributes = True

class MoodData(BaseModel):
    userId: int
    mood: str
    datetime: datetime

    class Config:
        from_attributes = True

class MoodPredictRequest(BaseModel):
    text: str
