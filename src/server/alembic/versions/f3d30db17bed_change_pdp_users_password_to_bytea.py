"""Change pdp_users.password to bytea

Revision ID: f3d30db17bed
Revises: 41da831646e4
Create Date: 2020-12-16 21:26:08.548724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3d30db17bed"
down_revision = "41da831646e4"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("pdp_users", "password")
    op.add_column("pdp_users", sa.Column("password", sa.Binary, nullable=False))


def downgrade():
    op.drop_column("pdp_users", "password")
    op.add_column("pdp_users", "password", sa.String(50), nullable=False),
