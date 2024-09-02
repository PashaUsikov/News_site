from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):
    __tablename__='users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    password: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(10), index=True)
    email: Mapped[str] = mapped_column(String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
       return '<User name={} id={}>'.format(self.username, self.id)