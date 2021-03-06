"""refactor

Revision ID: efb205bc5f79
Revises: a89ec4490d69
Create Date: 2019-07-08 12:02:58.054929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efb205bc5f79'
down_revision = 'a89ec4490d69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valve_configuration', sa.Column('configtype', sa.Integer(), nullable=False))
    op.drop_column('valve_configuration', 'configType')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valve_configuration', sa.Column('configType', sa.INTEGER(), nullable=False))
    op.drop_column('valve_configuration', 'configtype')
    # ### end Alembic commands ###
