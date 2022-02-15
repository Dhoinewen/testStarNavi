from hmac import compare_digest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


conn = create_engine('postgresql+psycopg2://postgres:123456@localhost/test21')
Session = sessionmaker()
session = Session(bind=conn)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    posts = relationship('Post', backref='user', lazy=True)
    password = Column(String(24), nullable=False)
    likes = relationship('Like', backref='user', lazy=True)

    def check_password(self, password):
        return compare_digest(password, self.password)

    def __repr__(self):
        return f'{self.nickname}'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    creator = Column(ForeignKey("users.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    liked = relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f'{self.text}'

    
class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    liked_by = Column(ForeignKey('users.id'), nullable=False)
    liked_post = Column(ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return f'by{self.liked_by}'


Base.metadata.create_all(bind=conn)
