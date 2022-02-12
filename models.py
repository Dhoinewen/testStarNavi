from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


conn = create_engine('postgresql+psycopg2://postgres:123456@localhost/test21')
Session = sessionmaker()
session = Session(bind=conn)

Base = declarative_base()


association = Table(
    'association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('posts.id', ondelete='CASCADE')),
    Column('post_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
    )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    posts = relationship('Post', backref='user_', lazy=True)
    likes = relationship(
        'Post', secondary=association,
        back_populates='liked', lazy=True,
        cascade="all, delete",
        passive_deletes=True
    )

    def __repr__(self):
        return f'{self.nickname}'


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    creator = Column((ForeignKey("users.id")))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    liked = relationship(
        'User', secondary=association,
        back_populates='likes', lazy=True
    )


    def __repr__(self):
        return f'{self.text}'


Base.metadata.create_all(bind=conn)
