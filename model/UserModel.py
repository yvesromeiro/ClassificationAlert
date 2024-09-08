import uuid

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID


Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(PGUUID, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    birthdate = Column(String)
    document = Column(String)
    gender = Column(String)
    telephone = Column(String)
    is_active = Column(Boolean)
    yearly_income = Column(Integer)
