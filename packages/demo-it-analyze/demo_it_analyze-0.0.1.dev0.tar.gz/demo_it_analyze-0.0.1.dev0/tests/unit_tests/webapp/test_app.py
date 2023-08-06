import os
import pathlib

import pytest

from demo_it_analyze.app import app
from demo_it_analyze.nlp.ner import Entity

TEST_DB = "test.db"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False
    app.config["BASEDIR"] = pathlib.Path(__file__).parent.parent.parent
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.config["BASEDIR"], TEST_DB
    )
    yield app.test_client()


def test_ner_route(client):
    response = client.post("/ner", data="piacere, silvio berlusconi")
    res_objs = response.get_json()
    assert len(res_objs) == 1
    ent = Entity.parse_raw(res_objs[0])
    assert ent.text == "silvio berlusconi"
    assert ent.start == 2
    assert ent.end == 4
    assert ent.label == "PER"
