"""Remove is_deleted column

Revision ID: 68e974f35c12
Revises: 241f5908223f
Create Date: 2024-12-01 18:39:45.896751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68e974f35c12'
down_revision = '241f5908223f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.drop_column('id_deleted')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_deleted', sa.BOOLEAN(), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)

    # ### end Alembic commands ###
