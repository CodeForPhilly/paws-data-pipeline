"""Shelterluv animal events table

Revision ID: 90f471ac445c
Revises: 9687db7928ee
Create Date: 2022-09-04 17:21:51.511030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90f471ac445c'
down_revision = '9687db7928ee'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
    "sl_event_types",
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("event_name", sa.Text, nullable=False),
    )
    
    op.create_table (
    "sl_animal_events",
    sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
    sa.Column("person_id", sa.Integer, nullable=False),
    sa.Column("animal_id", sa.Integer, nullable=False),
    sa.Column("event_type", sa.Integer, sa.ForeignKey('sl_event_types.id')),
    sa.Column("time", sa.BigInteger, nullable=False)
    )
    
    op.create_index('sla_idx', 'sl_animal_events', ['person_id'])



def downgrade():
    op.drop_table("sl_animal_events")
    op.drop_table("sl_event_types")