"""empty message

Revision ID: 38c719752e97
Revises: 80f1886b7378
Create Date: 2021-04-27 18:01:33.710095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38c719752e97'
down_revision = '80f1886b7378'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('common',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ru', sa.String(length=80), nullable=False),
    sa.Column('eng', sa.String(length=120), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('context', sa.String(length=225), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('common')
    # ### end Alembic commands ###