"""empty message

Revision ID: 11d022f1526
Revises: None
Create Date: 2015-02-25 16:41:50.349658

"""

# revision identifiers, used by Alembic.
revision = '11d022f1526'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('URL',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('long_address', sa.String(length=255), nullable=True),
    sa.Column('short_address', sa.String(length=255), nullable=True),
    sa.Column('owner', sa.Integer(), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timestamp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('ip_address', sa.String(length=60), nullable=True),
    sa.Column('user_agent', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('encrypted_password', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('timestamp')
    op.drop_table('URL')
    ### end Alembic commands ###
