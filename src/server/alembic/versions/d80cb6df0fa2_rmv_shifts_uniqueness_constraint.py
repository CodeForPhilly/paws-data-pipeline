"""rmv shifts uniqueness constraint

Revision ID: d80cb6df0fa2
Revises: 90f471ac445c
Create Date: 2023-03-18 16:22:23.282568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd80cb6df0fa2'
down_revision = '90f471ac445c'
branch_labels = None
depends_on = None

# It's probably more likely that a duplicate row is actually a real shift with a bad (dupe)
# like Saturday, Saturday instead of Saturday, Sunday 
# We really care about last shift so this is not critical

def upgrade():
    op.drop_constraint( "uq_shift", "volgisticsshifts") 

def downgrade():
    # op.create_unique_constraint( "uq_shift", "volgisticsshifts",  ["volg_id", "assignment", "from_date", "hours"] ) 
    # This will fail if you have any dupes
    # running 
    #    ALTER TABLE "public"."volgisticsshifts" ADD CONSTRAINT "uq_shift" UNIQUE( "volg_id", "assignment", "from_date", "hours" );
    # will fail and tell you of any dupes so you can fix

    pass
