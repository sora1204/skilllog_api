from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.category import get_category_by_id
from app.crud.study_log import (
    create_study_log,
    delete_study_log,
    get_study_log_by_id,
    get_study_logs_by_owner,
    update_study_log,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.study_log import StudyLogCreate, StudyLogRead, StudyLogUpdate

router = APIRouter(
    prefix="/study-logs",
    tags=["study-logs"],
)

@router.post(
    "",
    response_model=StudyLogRead,
    status_code=status.HTTP_201_CREATED,
)
def create_study_log_api(
    study_log_create: StudyLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if study_log_create.category_id is not None:
        category = get_category_by_id(
            db=db,
            category_id=study_log_create.category_id,
            owner_id=current_user.id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )

    study_log = create_study_log(
        db=db,
        study_log_create=study_log_create,
        owner_id=current_user.id,
    )

    return study_log


@router.get("", response_model=list[StudyLogRead])
def read_study_logs(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
    keyword: str | None = Query(default=None, min_length=1, max_length=100),
    min_minutes: int | None = Query(default=None, ge=1, le=1440),
    max_minutes: int | None = Query(default=None, ge=1, le=1440),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_logs = get_study_logs_by_owner(
        db=db,
        owner_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        keyword=keyword,
        min_minutes=min_minutes,
        max_minutes=max_minutes,
    )

    return study_logs


@router.get("/{log_id}", response_model=StudyLogRead)
def read_study_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_log = get_study_log_by_id(
        db=db,
        log_id=log_id,
        owner_id=current_user.id,
    )

    if study_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study log not found",
        )

    return study_log


@router.patch("/{log_id}", response_model=StudyLogRead)
def update_study_log_api(
    log_id: int,
    study_log_update: StudyLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_log = get_study_log_by_id(
        db=db,
        log_id=log_id,
        owner_id=current_user.id,
    )

    if study_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study log not found",
        )

    if study_log_update.category_id is not None:
        category = get_category_by_id(
            db=db,
            category_id=study_log_update.category_id,
            owner_id=current_user.id,
        )

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )

    updated_study_log = update_study_log(
        db=db,
        study_log=study_log,
        study_log_update=study_log_update,
    )

    return updated_study_log


@router.delete("/{log_id}")
def delete_study_log_api(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    study_log = get_study_log_by_id(
        db=db,
        log_id=log_id,
        owner_id=current_user.id,
    )

    if study_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study log not found",
        )

    delete_study_log(
        db=db,
        study_log=study_log,
    )

    return {
        "message": "Study log deleted",
    }