from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class VotesModel(Base):
    __tablename__ = 'votes'

    post_id = Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    post = relationship('Posts', lazy='joined')
    user_id = Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    user = relationship('UserModel', lazy='joined')