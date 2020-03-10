"""added sensordata table

Revision ID: 616497e8f56f
Revises: 
Create Date: 2020-03-03 15:45:20.025886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '616497e8f56f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sensor_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.String(length=64), nullable=True),
    sa.Column('gait', sa.Integer(), nullable=True),
    sa.Column('acc_x', sa.Float(), nullable=True),
    sa.Column('acc_y', sa.Float(), nullable=True),
    sa.Column('acc_z', sa.Float(), nullable=True),
    sa.Column('gyr_x', sa.Float(), nullable=True),
    sa.Column('gyr_y', sa.Float(), nullable=True),
    sa.Column('gyr_z', sa.Float(), nullable=True),
    sa.Column('mag_x', sa.Float(), nullable=True),
    sa.Column('mag_y', sa.Float(), nullable=True),
    sa.Column('mag_z', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sensor_data')
    # ### end Alembic commands ###
