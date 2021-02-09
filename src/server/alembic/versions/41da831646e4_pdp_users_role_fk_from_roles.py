"""pdp_users.role FK from roles

Revision ID: 41da831646e4
Revises: 72d50d531bd5
Create Date: 2020-12-16 15:53:28.514053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41da831646e4"
down_revision = "72d50d531bd5"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("pdp_users", "role")
    op.add_column(
        "pdp_users", sa.Column("role", sa.Integer, sa.ForeignKey("pdp_user_roles._id"))
    )


def downgrade():
    pass
