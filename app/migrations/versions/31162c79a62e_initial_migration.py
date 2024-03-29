"""Initial Migration

Revision ID: 31162c79a62e
Revises: 
Create Date: 2022-08-15 13:52:08.624779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31162c79a62e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('verification_code', 'isValid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('verification_code', sa.Column('isValid', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
