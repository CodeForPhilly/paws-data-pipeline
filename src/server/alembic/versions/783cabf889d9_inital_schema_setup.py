"""inital schema setup

Revision ID: 783cabf889d9
Revises: 
Create Date: 2020-12-16 01:47:43.686881

"""
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
import datetime


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

    op.create_table(
        'contact_types',
        sa.Column('contact_type_id', sa.String, primary_key=True)
    )

    op.execute("""insert into contact_types values ('PERSON'), ('ORGANIZATION');""")

    op.create_table(
        'pdp_contacts',
        sa.Column('_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('matching_id', sa.Integer, primary_key=True),
        sa.Column('source_type', sa.String, nullable=False),
        sa.Column('source_id', sa.String, nullable=False),
        sa.Column('contact_type_id', sa.String, sa.ForeignKey("contact_types.contact_type_id")),
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

    op.execute("""CREATE INDEX pdp_contacts_email_idx ON public.pdp_contacts USING btree (email);""")
    op.execute("""CREATE INDEX pdp_contacts_mobile_idx ON public.pdp_contacts USING btree (mobile);""")


def downgrade():
    pass