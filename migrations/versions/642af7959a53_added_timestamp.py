"""added timestamp

Revision ID: 642af7959a53
Revises: 616497e8f56f
Create Date: 2020-03-09 08:58:33.918281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642af7959a53'
down_revision = '616497e8f56f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sensor_data', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sensor_data', 'timestamp')
    # ### end Alembic commands ###