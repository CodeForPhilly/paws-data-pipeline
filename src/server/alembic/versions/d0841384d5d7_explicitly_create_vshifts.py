"""Explicitly create vshifts

Revision ID: d0841384d5d7
Revises: e3ef522bd3d9
Create Date: 2021-07-05 22:05:52.743905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0841384d5d7'
down_revision = 'e3ef522bd3d9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
        "volgisticsshifts",
        sa.Column("_id", sa.Integer, primary_key=True),
        sa.Column("volg_id", sa.Integer, nullable=False),
        sa.Column("assignment", sa.String(), nullable=True),
        sa.Column("site", sa.String(), nullable=True),      
        sa.Column("from_date",  sa.Date, nullable=False),
        sa.Column("hours",  sa.DECIMAL, nullable=False)
    )

    op.execute("""CREATE  INDEX vs_volg_id_idx 
                    ON public.volgisticsshifts USING btree (volg_id);"""
                    )

    op.create_unique_constraint( "uq_shift", "volgisticsshifts",  ["volg_id", "assignment", "from_date", "hours"] ) 


def downgrade():
    op.drop_table("volgisticsshifts")
