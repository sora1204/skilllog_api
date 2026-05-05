import os

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key-later-please-use-env-file",
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)