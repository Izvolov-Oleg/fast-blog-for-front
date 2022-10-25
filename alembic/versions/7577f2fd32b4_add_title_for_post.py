"""add title for post

Revision ID: 7577f2fd32b4
Revises: db6565fdb060
Create Date: 2022-10-25 15:05:52.233804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7577f2fd32b4'
down_revision = 'db6565fdb060'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'title')
    # ### end Alembic commands ###