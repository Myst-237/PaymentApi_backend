"""adding otp db object

Revision ID: ffcb166eaa11
Revises: ed52221529bb
Create Date: 2022-08-17 09:49:32.182986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffcb166eaa11'
down_revision = 'ed52221529bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('otp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=20), nullable=True),
    sa.Column('cardRef', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('otp')
    # ### end Alembic commands ###
