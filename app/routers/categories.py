from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.category import (
    create_category,
    delete_category,
    get_categories_by_owner,
    get_category_by_id,
    get_category_by_name,
    update_category,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.post(
    "",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_category_api(
    category_create: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_category = get_category_by_name(
        db=db,
        name=category_create.name,
        owner_id=current_user.id,
    )

    if existing_category is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )

    category = create_category(
        db=db,
        category_create=category_create,
        owner_id=current_user.id,
    )

    return category


@router.get("", response_model=list[CategoryRead])
def read_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    categories = get_categories_by_owner(
        db=db,
        owner_id=current_user.id,
    )

    return categories


@router.get("/{category_id}", response_model=CategoryRead)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_category_by_id(
        db=db,
        category_id=category_id,
        owner_id=current_user.id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category_api(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_category_by_id(
        db=db,
        category_id=category_id,
        owner_id=current_user.id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if category_update.name is not None:
        existing_category = get_category_by_name(
            db=db,
            name=category_update.name,
            owner_id=current_user.id,
        )

        if existing_category is not None and existing_category.id != category.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists",
            )

    updated_category = update_category(
        db=db,
        category=category,
        category_update=category_update,
    )

    return updated_category


@router.delete("/{category_id}")
def delete_category_api(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_category_by_id(
        db=db,
        category_id=category_id,
        owner_id=current_user.id,
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    delete_category(
        db=db,
        category=category,
    )

    return {
        "message": "Category deleted",
    }