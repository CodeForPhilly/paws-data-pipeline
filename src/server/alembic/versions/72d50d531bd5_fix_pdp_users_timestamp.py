"""Fix pdp_users timestamp

Revision ID: 72d50d531bd5
Revises: 783cabf889d9
Create Date: 2020-12-16 15:22:54.734670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = "72d50d531bd5"
down_revision = "783cabf889d9"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("pdp_users", "created")
    op.add_column(
        "pdp_users",
        sa.Column("created", sa.DateTime, nullable=False, server_default=func.now()),
    )


def downgrade():
    sa.Column("created", sa.DateTime, nullable=False, server_default="now()")
