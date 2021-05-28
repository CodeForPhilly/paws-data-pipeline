"""create execution status table

Revision ID: bfb1262d3195
Revises: 05e0693f8cbb
Create Date: 2021-05-28 16:12:40.561829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'bfb1262d3195'
down_revision = '05e0693f8cbb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table (
        "execution_status",
        sa.Column("_id", sa.Integer, primary_key=True),
        sa.Column("job_id", sa.Integer,  nullable=False),
        sa.Column("status", sa.String(32),   nullable=False),
        sa.Column("details", sa.String(128),  nullable=False),
        sa.Column("update_stamp", sa.DateTime,  nullable=False, server_default=func.now())
    )

    op.execute("""CREATE FUNCTION last_upd_trig() RETURNS trigger
                LANGUAGE plpgsql AS
                $$BEGIN
                NEW.update_stamp := current_timestamp;
                RETURN NEW;
                END;$$;""")

    op.execute("""CREATE TRIGGER last_upd_trigger
                BEFORE INSERT OR UPDATE ON execution_status
                FOR EACH ROW
                EXECUTE PROCEDURE last_upd_trig();"""
                )   # Postgres-specific, obviously 


def downgrade():
    op.drop_table("execution_status")
    op.execute("DROP FUNCTION last_upd_trig()")