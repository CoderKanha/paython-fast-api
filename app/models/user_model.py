from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text
from app.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, nullable=False, primary_key=True)
    username = Column('username', String, nullable=False)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    email = Column('email', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    is_deleted = Column('is_deleted', Boolean, nullable=False, server_default=text('False'))
    created_at = Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column('updated_at', TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
