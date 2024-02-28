"""Drop RFM tables

Revision ID: 18cb37abfbe7
Revises: d80cb6df0fa2
Create Date: 2024-02-06 12:00:00.711345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18cb37abfbe7'
down_revision = 'd80cb6df0fa2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('rfm_scores')
    op.drop_table('rfm_mapping')

def downgrade():
    pass
