"""Update rfm_mapping, remove rfm_edges

Revision ID: 40be910424f0
Revises: 57b547e9b464
Create Date: 2021-08-08 17:26:40.622536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40be910424f0'
down_revision = '57b547e9b464'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("rfm_edges")    # Unneeded, unused
    op.add_column('rfm_mapping',
        sa.Column('rfm_text_color', sa.String())
        )


def downgrade():
    op.create_table (
        "rfm_edges",
        sa.Column("component", sa.String(), primary_key=True),
        sa.Column("edge_string", sa.String(), nullable=False)
    )
