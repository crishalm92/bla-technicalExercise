from dotenv import dotenv_values
from app.repository.postgresql import SessionLocalPostgres
from app.repository.postgresql import Base as postgres_base
from app.repository.sqlite.config import SessionLocal as sl_sqlite
from app.repository.sqlite.config import Base as sql_base
from app.repository.sqlite.config import config_db
from app.repository.postgresql import init_db

config = dotenv_values()


def get_session_local():
    if config['DATABASE_ENGINE'] == 'postgres':
        init_db()
        return SessionLocalPostgres()
    if config['DATABASE_ENGINE'] == 'sqlite':
        config_db()
        return sl_sqlite()


def get_base_db_type():
    if config['DATABASE_ENGINE'] == 'postgres':
        from app.repository.postgresql import init_db
        init_db()
        return postgres_base
    if config['DATABASE_ENGINE'] == 'sqlite':
        config_db()
        return sql_base
