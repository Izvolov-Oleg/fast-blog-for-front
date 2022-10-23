import sqlalchemy as sa

from app.db.database import DBBase


class User(DBBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
