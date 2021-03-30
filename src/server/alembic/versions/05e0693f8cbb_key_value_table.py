"""key/value table

Revision ID: 05e0693f8cbb
Revises: 6b8cf99be000
Create Date: 2021-03-18 11:35:43.512082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05e0693f8cbb'
down_revision = '6b8cf99be000'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'kv_unique',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('keycol', sa.String(50), nullable=False, unique=True),
        sa.Column('valcol', sa.String(65536), nullable=True),
    )
    
    # op.create_index('kvk_ix', 'kv_unique', ['key'], unique=True)


def downgrade():
    pass
