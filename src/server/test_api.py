import os

import pytest

from app import create_app

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


@pytest.fixture
def app():
    return create_app(is_test=True)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def user_auth_hdr(client):
    data = {"username": "base_user", "password": BASEUSER_PW}

    response = client.post("/api/user/login", json=data)
    assert response.status_code == 200

    try:
        jwt_token = response.json["access_token"]
    except:
        pytest.fail("Did not get access token", pytrace=False)

    assert len(jwt_token) > 16
    b_string = "Bearer " + jwt_token
    return {"Authorization": b_string}


@pytest.fixture
def admin_auth_hdr(client):
    data = {"username": "base_admin", "password": BASEADMIN_PW}

    response = client.post("/api/user/login", json=data)
    assert response.status_code == 200

    try:
        jwt_token = response.json["access_token"]
    except:
        pytest.fail("Did not get access token", pytrace=False)

    assert len(jwt_token) > 16
    b_string = "Bearer " + jwt_token
    return {"Authorization": b_string}


# Simple API tests  ################################################
def test_usertest(client):
    """Verify liveness test works"""
    response = client.get("/api/user/test")
    assert response.status_code == 200


########   Dependent tests   #################################


def test_useraccess(client, user_auth_hdr):
    """Verify logged-in base_user can use JWT to access test_auth"""
    response = client.get("/api/user/test_auth", headers=user_auth_hdr)
    assert response.status_code == 200


def test_user_bad_pw(client):
    """Verify base_user with bad pw fails"""
    data = {"username": "base_user", "password": "some_bad_password"}

    response = client.post("/api/user/login", json=data)
    assert response.status_code == 401


def test_inact_userblocked(client):
    """Verify base_user_inact can't login because marked inactive."""
    # Same pw as base_user
    data = {"username": "base_user_inact", "password": BASEUSER_PW}
    response = client.post("/api/user/login", json=data)
    assert response.status_code == 401


###   Admin-level tests ######################################


def test_adminlogin(client):
    """Verify base_admin can log in/get JWT."""
    data = {"username": "base_admin", "password": BASEADMIN_PW}

    response = client.post("/api/user/login", json=data)
    assert response.status_code == 200

    try:
        jwt_token = response.json["access_token"]
    except:
        pytest.fail("Did not get access token", pytrace=False)

    assert len(jwt_token) > 16


def test_admingetusers(client, admin_auth_hdr):
    """Verify logged-in base_admin can use JWT to get user list"""
    response = client.get("/api/admin/user/get_users", headers=admin_auth_hdr)
    assert response.status_code == 200

    userlist = response.json
    assert len(response.json) > 1


def test_check_usernames(client, admin_auth_hdr):
    """Verify logged-in base_admin can test usernames, gets correct result - existing user"""
    data = {"username": "base_admin"}
    response = client.post(
        "/api/admin/user/check_name", headers=admin_auth_hdr, json=data
    )
    assert response.status_code == 200

    is_user = response.json
    assert is_user == 1


def test_check_badusernames(client, admin_auth_hdr):
    """Verify logged-in base_admin can test usernames, gets correct result - nonexistant user"""
    data = {"username": "got_no_username_like_this"}
    response = client.post(
        "/api/admin/user/check_name", headers=admin_auth_hdr, json=data
    )
    assert response.status_code == 200

    is_user = response.json
    assert is_user == 0


@pytest.mark.skip
def test_admin_currentFiles(client, admin_auth_hdr):
    """Verify admin user can get Current Files list"""
    response = client.get("/api/listCurrentFiles", headers=admin_auth_hdr)
    assert response.status_code == 200


def test_admin_statistics(client, admin_auth_hdr):
    """360 view Statistics"""
    response = client.get("/api/statistics", headers=admin_auth_hdr)
    assert response.status_code == 200


def test_usergetusers(client, user_auth_hdr):
    """Verify logged-in base_user *cannot* use JWT to get user list"""
    response = client.get("/api/admin/user/get_users", headers=user_auth_hdr)
    assert response.status_code == 403


@pytest.mark.skip
def test_currentFiles(client, admin_auth_hdr):
    """360 view Current Files list"""
    response = client.get("/api/listCurrentFiles", headers=admin_auth_hdr)
    assert response.status_code == 200


def test_statistics(client, admin_auth_hdr):
    """360 view Statistics"""
    response = client.get("/api/statistics", headers=admin_auth_hdr)
    assert response.status_code == 200


###   Shelterluv API tests ######################################


@pytest.mark.skipif(SL_Token, reason="Not run when SL_Token Present")
def test_user_get_person_animal_events(client, user_auth_hdr):
    """Test that the api returns mock data if the Shelterluv Token
    is missing from secrets
    """
    try:
        response = client.get(
            "/api/person/12345/animal/12345/events", headers=user_auth_hdr
        )
    except Exception as err:
        print(err)
    else:
        assert response.status_code == 200
        from api.fake_data import sl_mock_data

        assert response.json == sl_mock_data("events")


@pytest.mark.skipif(SL_Token, reason="Not run when SL_Token Present")
def test_user_get_animals(client, user_auth_hdr):
    """Test that the api returns mock data if the Shelterluv Token
    is missing from secrets
    """
    try:
        response = client.get("/api/person/12345/animals", headers=user_auth_hdr)
    except Exception as err:
        print(err)
    else:
        assert response.status_code == 200
        from api.fake_data import sl_mock_data

        assert response.json == sl_mock_data("animals")


@pytest.mark.skipif(not SL_Token, reason="Run when SL_Token Present")
def test_user_get_animals_sl_token(client, user_auth_hdr):
    """Test to confirm api does not return mock values if the Shelterluv Token
    is present in the secrets_dict file.
    Note this works on the assumption the SL token is not valid, and returns
    a default empty value

    >> This is tricky - if SL token is correct and person_id is valid, could get animal records returned.

    """
    try:
        response = client.get("/api/person/12345/animals", headers=user_auth_hdr)
    except Exception as err:
        print(err)
        pytest.fail("test_user_get_animals_sl_token - Request failed", pytrace=False)
    else:
        assert response.status_code == 200
        assert response.json == {"person_details": {}, "animal_details": {}}


@pytest.mark.skipif(not SL_Token, reason="Run when SL_Token Present")
def test_user_get_person_animal_events_sl_token(client, user_auth_hdr):
    """Test to confirm api does not return mock values if the Shelterluv Token
    is present in the secrets_dict file.
    Note this works on the assumption the SL token is not valid, and returns
    a default empty value
    """
    try:
        response = client.get(
            "/api/person/12345/animal/12345/events", headers=user_auth_hdr
        )
    except Exception as err:
        print(err)
        pytest.fail(
            "test_user_get_person_animal_events_sl_token - Request failed",
            pytrace=False,
        )
    else:
        assert response.status_code == 200
        assert response.json == {}
