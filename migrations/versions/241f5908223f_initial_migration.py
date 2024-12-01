"""Initial migration

Revision ID: 241f5908223f
Revises: d0c2470eb2f6
Create Date: 2024-12-01 10:06:08.719625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '241f5908223f'
down_revision = 'd0c2470eb2f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('id_deleted', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
