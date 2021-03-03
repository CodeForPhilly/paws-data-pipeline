"""Add pdp_users full_name

Revision ID: 36c4ecbfd11a
Revises: 7138d52f92d6
Create Date: 2020-12-18 15:28:17.367718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "36c4ecbfd11a"
down_revision = "7138d52f92d6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pdp_users", sa.Column("full_name", sa.String))


def downgrade():
    pass
