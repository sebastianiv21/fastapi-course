from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"


# after install psycopg2-binary
# user:password@host:port/database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/TodoAppDatabase"

# check same thread is set to false to allow multiple requests to
# be processed at the same time, its used with sqlite
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
