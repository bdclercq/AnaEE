"""remove tables

Revision ID: 26f4d64bec06
Revises: 66ec614371c9
Create Date: 2019-04-30 15:54:02.664000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26f4d64bec06'
down_revision = '66ec614371c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('valve_configuration',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('status', sa.BLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('fati')
    op.drop_table('system_configuration')
    op.drop_table('valve_config')
    op.drop_table('valve')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('valve',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fati_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['fati_id'], [u'fati.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('valve_config',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('valve_id', sa.INTEGER(), nullable=True),
    sa.Column('on_bit', sa.NUMERIC(), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['valve_id'], [u'valve.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('system_configuration',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=False),
    sa.Column('status', sa.BLOB(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fati',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('valve_configuration')
    # ### end Alembic commands ###
