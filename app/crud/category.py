from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category_by_id(
    db: Session,
    category_id: int,
    owner_id: int,
) -> Category | None:
    statement = select(Category).where(
        Category.id == category_id,
        Category.owner_id == owner_id,
    )
    return db.scalar(statement)


def get_category_by_name(
    db: Session,
    name: str,
    owner_id: int,
) -> Category | None:
    statement = select(Category).where(
        Category.name == name,
        Category.owner_id == owner_id,
    )
    return db.scalar(statement)


def get_categories_by_owner(
    db: Session,
    owner_id: int,
) -> list[Category]:
    statement = (
        select(Category)
        .where(Category.owner_id == owner_id)
        .order_by(Category.created_at.desc())
    )
    return list(db.scalars(statement).all())


def create_category(
    db: Session,
    category_create: CategoryCreate,
    owner_id: int,
) -> Category:
    category = Category(
        name=category_create.name,
        description=category_create.description,
        owner_id=owner_id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def update_category(
    db: Session,
    category: Category,
    category_update: CategoryUpdate,
) -> Category:
    update_data = category_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(category, field, value)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category: Category,
) -> None:
    db.delete(category)
    db.commit()