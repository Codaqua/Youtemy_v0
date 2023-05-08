from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
import os

# Get database URL from the environment or use a default URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:asturias@localhost/YoutemyApplicationDatabase"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Chat
# engine = create_engine(
#     DATABASE_URL,
#     poolclass=QueuePool,  # Use QueuePool for thread safety
#     pool_size=5,
#     max_overflow=5,
#     pool_timeout=30,
#     pool_recycle=1800,
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

