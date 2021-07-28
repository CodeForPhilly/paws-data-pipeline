"""Create RFM edges table

Revision ID: 57b547e9b464
Revises: 494e064d69a3
Create Date: 2021-07-20 21:39:00.438116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57b547e9b464'
down_revision = '494e064d69a3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
        "rfm_edges",
        sa.Column("component", sa.String(), primary_key=True),
        sa.Column("edge_string", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table("rfm_edges")
