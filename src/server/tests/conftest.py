import os

import pytest
import sqlalchemy as sa
from alembic.command import upgrade
from alembic.config import Config
from app import create_app
from pytest_postgresql import factories
from user_mgmt.base_users import create_base_roles, create_base_users

try:
    from secrets_dict import BASEADMIN_PW, BASEUSER_PW
except ImportError:
    BASEUSER_PW = os.environ["BASEUSER_PW"]
    BASEADMIN_PW = os.environ["BASEADMIN_PW"]


try:
    from secrets_dict import SHELTERLUV_SECRET_TOKEN
except ImportError:
    SHELTERLUV_SECRET_TOKEN = os.getenv("SHELTERLUV_SECRET_TOKEN")
finally:
    SL_Token = True if SHELTERLUV_SECRET_TOKEN else False


def loader(host, port, user, dbname, password):
    os.chdir("./src/server")
    cfg = Config("alembic.ini")
    db = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    cfg.set_main_option("sqlalchemy.url", db)
    # FIXME
    # cfg.attributes['test']
    upgrade(cfg, "head")
    engine = sa.create_engine(db)
    with engine.begin() as conn:
        create_base_roles(conn)  # IFF there are no roles already
        create_base_users(conn, engine)  # IFF there are no users already


pg_noproc = factories.postgresql_noproc(
    password="thispasswordisverysecure", load=[loader]
)
pg = factories.postgresql("pg_noproc")


@pytest.fixture
def app(pg):
    return create_app(is_test=True)
