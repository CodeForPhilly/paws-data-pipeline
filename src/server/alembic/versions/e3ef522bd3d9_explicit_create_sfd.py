"""Explicit creation for salesforcedonations

Revision ID: e3ef522bd3d9
Revises: bfb1262d3195
Create Date: 2021-06-18 21:55:56.651101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3ef522bd3d9'
down_revision = 'bfb1262d3195'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
        "salesforcedonations",
        sa.Column("_id", sa.Integer, primary_key=True),
        sa.Column("opp_id", sa.String(), nullable=False),
        sa.Column("recurring_donor", sa.Boolean,  nullable=False),
        sa.Column("primary_contact", sa.String(), nullable=True),
        sa.Column("contact_id", sa.String(), nullable=False),
        sa.Column("amount",  sa.DECIMAL, nullable=False),
        sa.Column("close_date",  sa.Date, nullable=False),
        sa.Column("donation_type",  sa.String(), nullable=True),        
        sa.Column("primary_campaign_source", sa.String(),nullable=True)
    )

    op.execute("""CREATE  INDEX sfd_contact_id_idx 
                    ON public.salesforcedonations USING btree (contact_id);"""
                    )

    op.create_unique_constraint( "uq_donation", "salesforcedonations",  ["opp_id", "contact_id", "close_date", "amount"] ) 


def downgrade():
    op.drop_table("salesforcedonations")