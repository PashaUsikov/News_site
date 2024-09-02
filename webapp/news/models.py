from datetime import datetime

from webapp.db import db

from webapp.user.models import User
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime


class News(db.Model):
    __tablename__='news'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    published: Mapped[datetime.datetime] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)
    picture: Mapped[str] = mapped_column(nullable=True)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self):
       return '<News {} {}>'.format(self.title, self.url)
    

class Comment(db.Model):
    __tablename__='comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())
    news_id: Mapped[int] = mapped_column(
        ForeignKey('news.id', ondelete='CASCADE'), index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True)
    news = relationship('News', backref='comments')
    users = relationship('User', backref='comments')

    
    def __repr__(self):
        return '<Comment {}>'.format(self.id)
    