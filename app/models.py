from .database import Base
from sqlalchemy import (Column, Integer, String, Boolean, 
                        ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("user.id",
                                          ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")

class User(Base):
    __tablename__ = "user"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text("now()"))

class Vote(Base):
    __tablename__ = 'vote'
    user_id = Column(Integer,
                     ForeignKey('user.id', ondelete='CASCADE'),
                     primary_key=True)
    post_id = Column(Integer,
                     ForeignKey('posts.id', ondelete='CASCADE'),
                     primary_key=True)