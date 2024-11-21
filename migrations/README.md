# Alembic migrations directory

This service uses Alembic for database migrations.

## Creating new revision

```shell
alembic revision --autogenerate -m "Some revision"
```

## Migrating to the latest revision

```shell
alembic upgrade head
```