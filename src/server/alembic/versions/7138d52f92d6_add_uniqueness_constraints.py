"""add uniqueness constraints

Revision ID: 7138d52f92d6
Revises: f3d30db17bed
Create Date: 2020-12-17 17:31:29.154789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7138d52f92d6"
down_revision = "f3d30db17bed"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("uq_username", "pdp_users", ["username"])
    op.create_unique_constraint("uq_role", "pdp_user_roles", ["role"])


def downgrade():
    pass
