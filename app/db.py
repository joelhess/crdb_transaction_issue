"""Provides the db connection."""

from functools import wraps
from typing import Any, Callable, Optional

import structlog
from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction

from base_models import BaseSQLModel

logger = structlog.get_logger(__name__)

database_url = "127.0.0.1:26257/roach"
database_user = "cockroach"
database_password = "arthropod"





class Database:
    """Database class."""

    def __init__(self, database_url, database_user, database_password) -> None:
        """Init DB properties."""
        self._db_url = database_url
        self._db_user = database_user
        self._db_password = database_password
        self.engine: Optional[Engine] = None
        # self.init_connection()

    def init_connection(self) -> Engine:
        """Init DB connection."""
        try:
            logger.info("Initializing database connection...")
            self.engine = create_engine(
                f"cockroachdb://{self._db_user}:{self._db_password}@{self._db_url}",
                echo=True,
            )
            logger.info("Initializing database connection...DONE")
            return self.engine
        except Exception as connection_error:
            logger.error("Initializing database connection...FAIL")
            raise

    def create_database(self) -> None:
        """Create all tables."""
        logger.info("Creating all tables...")
        BaseSQLModel.metadata.create_all(self.engine)  # type: ignore
        logger.info("Create all tables DONE")

    def delete_all_tables(self) -> None:
        """Delete all tables."""
        logger.info("Deleting all tables...")
        BaseSQLModel.metadata.drop_all(self.engine)  # type: ignore
        logger.info("Delete all tables DONE")

    def get_db_session(self) -> sessionmaker:
        session_local = sessionmaker(bind=self.engine)
        return session_local
    
db = Database(
    database_url=database_url,
    database_user=database_user,
    database_password=database_password,
)

def cockroach_transaction(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "db_session" in kwargs:
            return func(*args, **kwargs)
        else:
            # LOG.info("Running transaction", func=func.__name__)
            try:
                return run_transaction(
                    db.get_db_session(),
                    lambda s: func(*args, **kwargs, db_session=s),
                    max_retries=1,
                    max_backoff=4,
                )
            except Exception as e:
                # LOG.error("Transaction failed", func=func.__name__, error=e)
                raise

    return wrapper
