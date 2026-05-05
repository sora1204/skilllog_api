from datetime import date

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.study_log import StudyLog
from app.schemas.study_log import StudyLogCreate, StudyLogUpdate


def get_study_log_by_id(
    db: Session,
    log_id: int,
    owner_id: int,
) -> StudyLog | None:
    statement = select(StudyLog).where(
        StudyLog.id == log_id,
        StudyLog.owner_id == owner_id,
    )
    return db.scalar(statement)


def get_study_logs_by_owner(
    db: Session,
    owner_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    category_id: int | None = None,
    keyword: str | None = None,
    min_minutes: int | None = None,
    max_minutes: int | None = None,
) -> list[StudyLog]:
    statement = select(StudyLog).where(
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

    if category_id is not None:
        statement = statement.where(
            StudyLog.category_id == category_id
        )

    if keyword is not None:
        keyword_pattern = f"%{keyword}%"

        statement = statement.where(
            or_(
                StudyLog.title.ilike(keyword_pattern),
                StudyLog.resource.ilike(keyword_pattern),
                StudyLog.note.ilike(keyword_pattern),
                StudyLog.reflection.ilike(keyword_pattern),
            )
        )

    if min_minutes is not None:
        statement = statement.where(
            StudyLog.minutes >= min_minutes
        )

    if max_minutes is not None:
        statement = statement.where(
            StudyLog.minutes <= max_minutes
        )

    statement = statement.order_by(
        StudyLog.study_date.desc(),
        StudyLog.created_at.desc(),
    )

    return list(db.scalars(statement).all())


def create_study_log(
    db: Session,
    study_log_create: StudyLogCreate,
    owner_id: int,
) -> StudyLog:
    study_log = StudyLog(
        owner_id=owner_id,
        category_id=study_log_create.category_id,
        study_date=study_log_create.study_date,
        title=study_log_create.title,
        minutes=study_log_create.minutes,
        resource=study_log_create.resource,
        resource_url=(
            str(study_log_create.resource_url)
            if study_log_create.resource_url is not None
            else None
        ),
        note=study_log_create.note,
        reflection=study_log_create.reflection,
        understanding_level=study_log_create.understanding_level,
    )

    db.add(study_log)
    db.commit()
    db.refresh(study_log)

    return study_log


def update_study_log(
    db: Session,
    study_log: StudyLog,
    study_log_update: StudyLogUpdate,
) -> StudyLog:
    update_data = study_log_update.model_dump(exclude_unset=True)

    if "resource_url" in update_data and update_data["resource_url"] is not None:
        update_data["resource_url"] = str(update_data["resource_url"])

    for field, value in update_data.items():
        setattr(study_log, field, value)

    db.add(study_log)
    db.commit()
    db.refresh(study_log)

    return study_log


def delete_study_log(
    db: Session,
    study_log: StudyLog,
) -> None:
    db.delete(study_log)
    db.commit()