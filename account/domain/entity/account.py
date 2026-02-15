from sqlalchemy import Column, Integer, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from account.domain.value_objects.login_type import LoginType
from config.mysql_config import MySQLConfig

Base = MySQLConfig().get_base()

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login_type = Column(Enum(LoginType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("AccountProfile", back_populates="account", uselist=False)
