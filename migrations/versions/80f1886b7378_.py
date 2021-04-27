"""empty message

Revision ID: 80f1886b7378
Revises: 3bcafa9000a0
Create Date: 2021-04-27 18:01:25.927094

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '80f1886b7378'
down_revision = '3bcafa9000a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Сommon')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Сommon',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ru', mysql.VARCHAR(collation='utf8_unicode_ci', length=80), nullable=False),
    sa.Column('eng', mysql.VARCHAR(collation='utf8_unicode_ci', length=120), nullable=False),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.Column('context', mysql.VARCHAR(collation='utf8_unicode_ci', length=225), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_unicode_ci',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
