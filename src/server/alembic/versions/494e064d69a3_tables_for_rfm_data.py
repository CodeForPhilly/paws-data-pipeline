"""Tables for RFM data

Revision ID: 494e064d69a3
Revises: d0841384d5d7
Create Date: 2021-07-20 19:45:29.418756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '494e064d69a3'
down_revision = 'd0841384d5d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
        "rfm_scores",
        sa.Column("matching_id", sa.Integer, primary_key=True),
        sa.Column("rfm_score", sa.String(3), nullable=False)
    )

    op.create_table (
        "rfm_mapping",
        sa.Column("rfm_value", sa.String(3), primary_key=True),
        sa.Column("rfm_label", sa.String(), nullable=True),
        sa.Column("rfm_color", sa.String(), nullable=True, default='0xe0e0e0')
    )


def downgrade():
    op.drop_table("rfm_scores")
    op.drop_table("rfm_mapping")
