"""empty message

Revision ID: 4107af95d07
Revises: 3bc54415868
Create Date: 2015-02-21 10:26:38.416602

"""

# revision identifiers, used by Alembic.
revision = '4107af95d07'
down_revision = '3bc54415868'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmark', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bookmark', 'user', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookmark', type_='foreignkey')
    op.drop_column('bookmark', 'user_id')
    ### end Alembic commands ###
