"""empty message

Revision ID: 8fd2803571
Revises: None
Create Date: 2015-02-24 23:34:56.727268

"""

# revision identifiers, used by Alembic.
revision = '8fd2803571'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('encrypted_password', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_link', sa.String(length=255), nullable=False),
    sa.Column('short_link', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_link')
    )
    op.create_table('click',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(length=255), nullable=True),
    sa.Column('click_agent', sa.String(length=255), nullable=True),
    sa.Column('link_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('clicker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clicker_id'], ['click.id'], ),
    sa.ForeignKeyConstraint(['link_id'], ['link.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('custom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_link', sa.String(length=255), nullable=True),
    sa.Column('new_link', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['start_link'], ['link.short_link'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('new_link')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('custom')
    op.drop_table('click')
    op.drop_table('link')
    op.drop_table('user')
    ### end Alembic commands ###
