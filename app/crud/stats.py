from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.study_log import StudyLog

def get_total_stats(
        db: Session,
        owner_id: int,
) -> dict:
    statement = select(
        func.coalesce(func.sum(StudyLog.minutes), 0).label("total_minutes"),
        func.count(StudyLog.id).label("log_count"),
    ).where(
        StudyLog.owner_id == owner_id
    )

    result = db.execute(statement).one()

    total_minutes = int(result.total_minutes)
    log_count = int(result.log_count)

    return{
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "log_count": log_count,
    }

def get_monthly_stats(
        db: Session,
        owner_id: int,
        start_date: date,
        end_date:date,
) -> dict:
    statement = select(
        func.coalesce(func.sum(StudyLog.minutes), 0).label("total_minutes"),
        func.count(StudyLog.id).label("log_count"),
    ).where(
        StudyLog.owner_id == owner_id,
        StudyLog.study_date >= start_date,
        StudyLog.study_date < end_date,
    )

    result = db.execute(statement).one()

    total_minutes = int(result.total_minutes)
    log_count = int(result.log_count)

    return{
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "log_count": log_count,
    }

def get_stats_by_category(
    db: Session,
    owner_id: int
) -> list[dict]:
    statement = (
        select(
            StudyLog.category_id.label("category_id"),
            Category.name.label("category_name"),
            func.coalesce(func.sum(StudyLog.minutes), 0).label("total_minutes"),
            func.count(StudyLog.id).label("log_count"),
        )
        .outerjoin(Category, StudyLog.category_id == Category.id)
        .where(StudyLog.owner_id == owner_id)
        .group_by(StudyLog.category_id, Category.name)
        .order_by(func.sum(StudyLog.minutes).desc())
    )

    rows = db.execute(statement).all()

    return[
        {
            "category_id": row.category_id,
            "category_name": row.category_name if row.category_name is not None else "未分類",
            "total_minutes": int(row.total_minutes),
            "total_hours": round(int(row.total_minutes) / 60, 2),
            "log_count": int(row.log_count),
        }
        for row in rows
    ]

def get_summary_stats(
        db: Session,
        owner_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
) -> dict:
    statement = select(
        func.coalesce(func.sum(StudyLog.minutes), 0).label("total_minutes"),
        func.count(StudyLog.id).label("log_count"),
    ).where(
        StudyLog.owner_id == owner_id
    )

    if start_date is not None:
        statement = statement.where(
            StudyLog.study_date >= start_date
        )

    if end_date is not None:
        statement = statement.where(
            StudyLog.study_date <= end_date
        )

    result = db.execute(statement).one()

    total_minutes = int(result.total_minutes)
    log_count = int(result.log_count)

    average_minutes_per_log = 0.0
    if log_count > 0:
        average_minutes_per_log = round(total_minutes / log_count, 2)

    return{
        "start_date": start_date,
        "end_date": end_date,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
        "log_count": log_count,
        "average_minutes_per_log": average_minutes_per_log,
    }