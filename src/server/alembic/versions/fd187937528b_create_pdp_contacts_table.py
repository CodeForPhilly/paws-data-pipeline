"""create pdp_contacts table

Revision ID: fd187937528b
Revises: 57b547e9b464
Create Date: 2021-08-10 20:16:54.169168

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
import datetime

# revision identifiers, used by Alembic.
revision = 'fd187937528b'
down_revision = '57b547e9b464'
branch_labels = None
depends_on = None


def upgrade():
    
    op.create_table('pdp_contact_types',
        sa.Column('contact_type_id', sa.String, primary_key=True)
    )

    op.execute("""insert into pdp_contact_types values ('PERSON'), ('ORGANIZATION');""")

    op.create_table('pdp_contacts',
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('matching_id', sa.Integer, primary_key=True),
        sa.Column('source_type', sa.String, nullable=False),
        sa.Column('source_id', sa.String, nullable=False),
        sa.Column('contact_type_id', sa.String, sa.ForeignKey("pdp_contact_types.contact_type_id")),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('email', sa.String),
        sa.Column('mobile', sa.String),
        sa.Column('street_and_number', sa.String),
        sa.Column('apartment', sa.String),
        sa.Column('city', sa.String),
        sa.Column('state', sa.String),
        sa.Column('zip', sa.String),
        sa.Column('json', JSONB),
        sa.Column('created_date', sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column('archived_date', sa.DateTime, default=None)
    )

def downgrade():
    
    op.drop_table("pdp_contacts")
    op.drop_table("pdp_contact_types")
