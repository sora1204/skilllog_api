from datetime import date
from pydantic import BaseModel

class TotalStatsRead(BaseModel):
    total_minutes: int
    total_hours: float
    log_count: int

class MonthlyStatsRead(BaseModel):
    year: int
    month: int
    total_minutes: int
    total_hours: float
    log_count: int

class CategoryStatsRead(BaseModel):
    category_id: int | None
    category_name: str
    total_minutes: int
    total_hours: float
    log_count: int

class SummaryStatsRead(BaseModel):
    start_date: date | None
    end_date: date | None
    total_minutes: int
    total_hours: float
    log_count: int
    average_minutes_per_log: float