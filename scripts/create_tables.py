from app.db.base import Base
from app.db.database import engine
from app.models import Category, StudyLog, User

def main():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    main()