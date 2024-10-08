"""empty message

Revision ID: 4ebd65da52eb
Revises: 
Create Date: 2024-10-01 15:32:10.328272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ebd65da52eb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node_network_receive_bytes_total',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nodename', sa.Text(), nullable=True),
    sa.Column('job', sa.Text(), nullable=True),
    sa.Column('instance', sa.Text(), nullable=True),
    sa.Column('summa', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node_network_transmit_bytes_total',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nodename', sa.Text(), nullable=True),
    sa.Column('job', sa.Text(), nullable=True),
    sa.Column('instance', sa.Text(), nullable=True),
    sa.Column('summa', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('node_uname_info',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('nodename', sa.Text(), nullable=True),
    sa.Column('job', sa.Text(), nullable=True),
    sa.Column('instance', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('user_id_tg', sa.BigInteger(), nullable=False),
    sa.Column('tg_name', sa.String(length=100), nullable=False),
    sa.Column('full_name', sa.String(length=100), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('update_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('users_id')
    )
    op.create_table('logmessage',
    sa.Column('logmessage_id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('type_message', sa.String(length=10), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['users_id'], ['users.users_id'], ),
    sa.PrimaryKeyConstraint('logmessage_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logmessage')
    op.drop_table('users')
    op.drop_table('node_uname_info')
    op.drop_table('node_network_transmit_bytes_total')
    op.drop_table('node_network_receive_bytes_total')
    # ### end Alembic commands ###
