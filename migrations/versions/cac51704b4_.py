"""empty message

Revision ID: cac51704b4
Revises: 4ed431e43b8
Create Date: 2015-02-23 13:06:30.069652

"""

# revision identifiers, used by Alembic.
revision = 'cac51704b4'
down_revision = '4ed431e43b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('links', 'short',
               existing_type=sa.VARCHAR(length=6),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('links', 'short',
               existing_type=sa.VARCHAR(length=6),
               nullable=True)
    ### end Alembic commands ###
