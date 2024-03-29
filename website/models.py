from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from struct import *

db = SQLAlchemy()
Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'

    note_id = Column(Integer, primary_key=True)
    note_text = Column(String(10000))
    date_created = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"))

    def __repr__(self):
        return f'Note: {self.note_text[:50]}...'

class Users(Base, UserMixin):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    firstName = Column(String(150))
    lastName = Column(String(150))
    password = Column(String(150))
    face_image = relationship("FaceReference", uselist=False)
    notes = relationship("Note", backref="user", lazy="dynamic")

    def __repr__(self):
        return f'User: {self.user_id} {self.firstName} {self.lastName} {self.password}'
    
    def get_id(self):
        return str(self.user_id)

class FaceReference(Base):
    __tablename__ = 'face_reference'

    photo_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    image = Column(LargeBinary, nullable=False)
    user = relationship("Users", back_populates="face_image")

    def __repr__(self):
        return f'FaceReference: {self.photo_id}'