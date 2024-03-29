"""adding phoneNumber verification

Revision ID: e33687354412
Revises: ffcb166eaa11
Create Date: 2022-08-17 12:16:24.876366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e33687354412'
down_revision = 'ffcb166eaa11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('phone_number',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=20), nullable=True),
    sa.Column('codeRef', sa.String(length=20), nullable=True),
    sa.Column('isValid', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phone_number')
    # ### end Alembic commands ###
