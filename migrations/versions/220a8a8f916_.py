"""empty message

Revision ID: 220a8a8f916
Revises: 211e9ccc70f
Create Date: 2015-02-21 16:48:13.565553

"""

# revision identifiers, used by Alembic.
revision = '220a8a8f916'
down_revision = '211e9ccc70f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clicks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('link_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['link_id'], ['links.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clicks')
    ### end Alembic commands ###
