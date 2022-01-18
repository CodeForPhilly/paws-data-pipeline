"""Remove execution_status.details field size limit

Revision ID: a3ba63dee8f4
Revises: 40be910424f0
Create Date: 2021-09-18 18:14:48.044985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3ba63dee8f4'
down_revision = '40be910424f0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('execution_status',"details", type_=sa.String(None) )



def downgrade():
    op.alter_column('execution_status',"details", type_=sa.String(128) )

