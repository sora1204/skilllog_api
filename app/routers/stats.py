from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud.stats import (
    get_monthly_stats,
    get_stats_by_category,
    get_summary_stats,
    get_total_stats,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.stats import (
    CategoryStatsRead,
    MonthlyStatsRead,
    SummaryStatsRead,
    TotalStatsRead,
)

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)


@router.get("/total", response_model=TotalStatsRead)
def read_total_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_total_stats(
        db=db,
        owner_id=current_user.id,
    )


@router.get("/monthly", response_model=MonthlyStatsRead)
def read_monthly_stats(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    stats = get_monthly_stats(
        db=db,
        owner_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )

    return {
        "year": year,
        "month": month,
        **stats,
    }


@router.get("/by-category", response_model=list[CategoryStatsRead])
def read_stats_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_stats_by_category(
        db=db,
        owner_id=current_user.id,
    )


@router.get("/summary", response_model=SummaryStatsRead)
def read_summary_stats(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_summary_stats(
        db=db,
        owner_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )