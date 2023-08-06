import typing as _t
import unittest as _ut
import sqlalchemy_utils as _su
import sqlalchemy as _sa
import sqlalchemy.engine as _sae
import pytest as _pytest
from . import app as _app
from . import types as _types
from .__test__.db import models as _m

_TC = _ut.TestCase()


def test_create_drop_test_db(sldb_test_url, sldb_test_schema_module):
    response = _app.create_db(
        _types.CreateDbArgs(
            url=sldb_test_url,
            append_name="test append",
            with_timestamp=True,
            schema=_types.SchemaDef(type="sqlalchemy", value=sldb_test_schema_module),
            seeds=[
                _types.SeedData(
                    type="module", value="sl.dbserver.__test__:seeds/test01.json"
                )
            ],
        )
    )
    _TC.assertTrue(_su.database_exists(response.url))

    # check that the tables were created
    engine = _sae.create_engine(response.url)
    with engine.connect() as connection:
        all_users = connection.execute(_sa.select(_m.User)).all()
    _TC.assertEqual(
        all_users,
        [
            (1, "user1", "user1@email.com"),
            (2, "user2", "user2@email.com"),
        ],
    )
    engine.dispose()

    # destroy the database, afterwards
    _app.drop_db(_types.DropDbArgs(drop_id=response.drop_id))
    _TC.assertFalse(_su.database_exists(response.url))


class TestSqlLoad:
    @_pytest.fixture(scope="function")
    def sldb_test_seed_data(self):
        return [
            _types.SeedData(
                type="module", value="sl.dbserver.__test__:seeds/test01.sql"
            ),
        ]

    def test_load_sql_seed(self, sldb_conn):
        all_users = sldb_conn.execute(_sa.select(_m.User)).all()
        _TC.assertEqual(
            all_users,
            [
                (1, "user1", "user1@email.com"),
                (2, "user2", "user2@email.com"),
            ],
        )
