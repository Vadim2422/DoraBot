"""empty message

Revision ID: 4aceeabda5b6
Revises: 
Create Date: 2023-08-20 14:16:37.263330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4aceeabda5b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('selection_msg_id', sa.Integer(), nullable=True),
    sa.Column('file_id', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_dora', sa.Boolean(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('links',
    sa.Column('link', sa.String(length=250), nullable=False),
    sa.Column('file_id', sa.String(length=150), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('is_dataset', sa.Boolean(), nullable=True),
    sa.Column('is_cool', sa.Boolean(), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.user_id'], ),
    sa.PrimaryKeyConstraint('link')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('links')
    op.drop_table('users')
    op.drop_table('admins')
    # ### end Alembic commands ###