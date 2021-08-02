from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    tgid = Column(String, unique=True)
    page = Column(Integer, default=0)
    created_on = Column(DateTime, default=datetime.utcnow)
