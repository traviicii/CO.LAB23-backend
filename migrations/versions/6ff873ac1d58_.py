"""empty message

Revision ID: 6ff873ac1d58
Revises: 5b9017255b14
Create Date: 2023-10-16 23:48:13.566805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6ff873ac1d58'
down_revision = '5b9017255b14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('duration', sa.String(length=50), nullable=True),
    sa.Column('industries', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('admin_timezone', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('hours_wk', sa.String(length=100), nullable=True),
    sa.Column('looking_for', sa.String(length=500), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.Column('team_size', sa.Integer(), nullable=True),
    sa.Column('need_pm', sa.Boolean(), nullable=True),
    sa.Column('need_designer', sa.Boolean(), nullable=True),
    sa.Column('need_dev', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('projects')
    # ### end Alembic commands ###
