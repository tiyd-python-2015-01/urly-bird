"""empty message

Revision ID: 4f9a749b5a3
Revises: 2c18c6696ee
Create Date: 2015-02-25 01:56:45.902143

"""

# revision identifiers, used by Alembic.
revision = '4f9a749b5a3'
down_revision = '2c18c6696ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('click', sa.Column('time_clicked', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('click', 'time_clicked')
    ### end Alembic commands ###
