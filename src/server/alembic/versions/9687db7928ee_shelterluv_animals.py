"""empty message

Revision ID: 9687db7928ee
Revises: a3ba63dee8f4
Create Date: 2021-12-24 21:15:33.399197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9687db7928ee'
down_revision = 'a3ba63dee8f4'
branch_labels = None
depends_on = None


def upgrade():
        op.create_table (
        "shelterluv_animals",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("local_id", sa.BigInteger, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("type",  sa.Text, nullable=False),
        sa.Column("dob", sa.BigInteger, nullable=False),
        sa.Column("update_stamp", sa.BigInteger, nullable=False),
        sa.Column("photo", sa.Text, nullable=False)
    )


def downgrade():
    op.drop_table("shelterluv_animals")
