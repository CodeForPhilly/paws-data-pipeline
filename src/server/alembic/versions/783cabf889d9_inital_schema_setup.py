"""inital schema setup

Revision ID: 783cabf889d9
Revises: 
Create Date: 2020-12-16 01:47:43.686881

"""
from sqlalchemy.sql.expression import null
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '783cabf889d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pdp_user_roles',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('role', sa.String(50), nullable=False)
    )

    op.create_table(
        'pdp_users',
        sa.Column('_id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False),
        sa.Column('active', sa.String(50), nullable=False),
        sa.Column('created', sa.DateTime,nullable=False, server_default='now()')
    )

def downgrade():
    pass