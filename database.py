from config import settings

CONNECTION_STRING_LOCAL_POSTGRES = (
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
)