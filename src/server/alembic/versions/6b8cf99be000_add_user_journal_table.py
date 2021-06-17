"""Add user journal table

Revision ID: 6b8cf99be000
Revises: 36c4ecbfd11a
Create Date: 2020-12-21 15:08:07.784568

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = "6b8cf99be000"
down_revision = "36c4ecbfd11a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pdp_user_journal",
        sa.Column("_id", sa.Integer, primary_key=True),
        sa.Column("stamp", sa.DateTime, nullable=False, server_default=func.now()),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("event_type", sa.String(50)),
        sa.Column("detail", sa.String(120)),
    )


def downgrade():
    op.drop_table('pdp_user_journal')
