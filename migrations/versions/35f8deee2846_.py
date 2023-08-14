"""empty message

Revision ID: 35f8deee2846
Revises: 0920dfc79404
Create Date: 2023-02-04 16:24:01.258382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35f8deee2846'
down_revision = '0920dfc79404'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('floor', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('roomtype', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('slots', sa.Integer(), nullable=True))
        batch_op.alter_column('maxOccupancy',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.alter_column('occupants',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.alter_column('occupants',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('maxOccupancy',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.drop_column('slots')
        batch_op.drop_column('roomtype')
        batch_op.drop_column('price')
        batch_op.drop_column('floor')

    # ### end Alembic commands ###
