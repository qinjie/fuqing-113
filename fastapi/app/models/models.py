from sqlalchemy import Column, DateTime, ForeignKey, String, TIMESTAMP, text, Boolean, Integer
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Guest(Base):
    __tablename__ = 'guest'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(256), nullable=True)
    alt_name = Column(String(256), nullable=True)
    salute = Column(String(10), nullable=True)
    title = Column(String(128), nullable=True)
    organization = Column(String(256), nullable=True)
    country = Column(String(128), nullable=True)
    email = Column(String(256), nullable=True)
    phone = Column(String(256), nullable=True)
    details = Column(String(1024), nullable=True,
                     comment='Details in JSON String')
    hash = Column(String(10), nullable=True, unique=True,
                  comment='hashlib.sha1("my message".encode("UTF-8")).hexdigest()[:10]')
    is_deleted = Column(Boolean, nullable=True, default=0)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Define the relationship between Guest and Task
    tasks = relationship("Task", back_populates="guest")


class Task(Base):
    __tablename__ = 'task'

    id = Column(INTEGER, primary_key=True)
    guest_id = Column(ForeignKey('guest.id', ondelete='CASCADE',
                      onupdate='CASCADE'), nullable=False, index=True)
    serial = Column(Integer, nullable=True)
    date_time = Column(DateTime, nullable=True)
    name = Column(String(256), nullable=False)
    details = Column(String(512), nullable=True)
    created_at = Column(TIMESTAMP, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=True,
                        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Define the relationship between Task and Guest
    guest = relationship("Guest", back_populates="tasks")
