import sqlalchemy as sa

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True, nullable=False)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(32), nullable=False)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=func.now(),
                           onupdate=func.now())


class Comment(Base):
    __tablename__ = 'comments'

    id = sa.Column(sa.Integer, primary_key=True)
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=func.now(),
                           onupdate=func.now())
    post_id = sa.Column(sa.Integer, sa.ForeignKey("posts.id"))
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('comments.id'))
