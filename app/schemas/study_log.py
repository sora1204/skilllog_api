from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StudyLogBase(BaseModel):
    study_date: date
    title: str = Field(..., min_length=1, max_length=100)
    category_id: int | None = None
    minutes: int = Field(..., ge=1, le=1440)
    resource: str | None = Field(default=None, max_length=100)
    resource_url: HttpUrl | None = None
    note: str | None = None
    reflection: str | None = None
    understanding_level: int | None = Field(default=None, ge=1, le=5)


class StudyLogCreate(StudyLogBase):
    pass


class StudyLogUpdate(BaseModel):
    study_date: date | None = None
    title: str | None = Field(default=None, min_length=1, max_length=100)
    category_id: int | None = None
    minutes: int | None = Field(default=None, ge=1, le=1440)
    resource: str | None = Field(default=None, max_length=100)
    resource_url: HttpUrl | None = None
    note: str | None = None
    reflection: str | None = None
    understanding_level: int | None = Field(default=None, ge=1, le=5)


class StudyLogRead(StudyLogBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)