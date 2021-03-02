import pytest, socket, requests, os

from secrets import BASEUSER_PW, BASEADMIN_PW

jwt_token = ''

#
# Run 'pytest' from the command line
#
# Running pytest can result in six different exit codes:
#   0 - All tests were collected and passed successfully
#   1 - Tests were collected and run but some of the tests failed
#   2 - Test execution was interrupted by the user
#   3 - Internal error happened while executing tests
#   4 - pytest command line usage error
#   5 - No tests were collected
#
# These codes are represented by the pytest.ExitCode enum


if os.getenv("IS_LOCAL") == "True":
    SERVER_URL = "http://localhost:3333"
    IS_LOCAL = True
else:
    SERVER_URL = "http://server:5000"
    IS_LOCAL = False

###  DNS lookup tests  ##############################

def test_bad_dns():
    """Verify DNS not resolving bad host names."""
    with pytest.raises(socket.gaierror):
        socket.getaddrinfo("bad_server_name_that_should_not_resolve", "5000")


@pytest.mark.skipif(IS_LOCAL, reason="Not run when IS_LOCAL")
def test_db_dns():
    """Verify we get IP for DB server."""

    # getaddrinfo works for IPv4 and v6
    try:
        gai = socket.getaddrinfo("db", "5000")
    except:
        pytest.fail('getaddrinfo() failed for db', pytrace=False)

    assert len(gai) > 0


@pytest.mark.skipif(IS_LOCAL, reason="Not run when IS_LOCAL")
def test_server_dns():
    """Verify we get IP for API server."""
    try:
        gai = socket.getaddrinfo("server", "5000")
    except socket.gaierror:
        pytest.fail('getaddrinfo() failed for server', pytrace=False)

    assert len(gai) > 0


@pytest.mark.skipif(IS_LOCAL, reason="Not run when IS_LOCAL")
def test_client_dns():
    """Verify we get IP for client."""
    try:
        gai = socket.getaddrinfo("client", "5000")
    except socket.gaierror:
        pytest.fail('getaddrinfo() failed for client', pytrace=False)

    assert len(gai) > 0

# Simple API tests  ################################################


def test_currentFiles():
    """360 view Current Files list"""
    response = requests.get(SERVER_URL + "/api/listCurrentFiles")
    assert response.status_code == 200


def test_statistics():
    """360 view Statistics"""
    response = requests.get(SERVER_URL + "/api/statistics")
    assert response.status_code == 200


def test_usertest():
    """Verify liveness test works"""
    response = requests.get(SERVER_URL + "/api/user/test")
    assert response.status_code == 200

########   Dependent tests   #################################

#      Store info across tests
class State:
    def __init__(self):
        self.state = {}

@pytest.fixture(scope='session')
def state() -> State:
    state = State()
    state.state['from_fixture'] = 0
    return state


def test_userlogin(state: State):
    """Verify base_user can log in/get JWT."""
    data = {"username":"base_user", "password" : BASEUSER_PW}

    response = requests.post(SERVER_URL + "/api/user/login", json=data)
    assert response.status_code == 200

    try:
        jwt_token = response.json()['access_token']
    except:
        pytest.fail('Did not get access token',  pytrace=False)

    assert len(jwt_token) > 16

    # Store the token for later use
    state.state['base_user'] = jwt_token


def test_useraccess(state: State):
    """Verify logged-in base_user can use JWT to access test_auth"""
    # Build auth string value including token from state
    b_string = 'Bearer ' + state.state['base_user']

    assert len(b_string) > 24

    auth_hdr = {'Authorization' : b_string}
    response = requests.get(SERVER_URL + "/api/user/test_auth", headers=auth_hdr)
    assert response.status_code == 200


def test_user_bad_pw():
    """Verify base_user with bad pw fails"""
    data = {"username":"base_user", "password" : 'some_bad_password'}

    response = requests.post(SERVER_URL + "/api/user/login", json=data)
    assert response.status_code == 401


def test_inact_userblocked(state: State):
    """Verify base_user_inact can't login because marked inactive."""
    # Same pw as base_user
    data = {"username":"base_user_inact", "password" : BASEUSER_PW}
    response = requests.post(SERVER_URL + "/api/user/login", json=data)
    assert response.status_code == 401


###   Admin-level tests ######################################

def test_adminlogin(state: State):
    """Verify base_admin can log in/get JWT."""
    data = {"username":"base_admin", "password" : BASEADMIN_PW}

    response = requests.post(SERVER_URL + "/api/user/login", json=data)
    assert response.status_code == 200

    try:
        jwt_token = response.json()['access_token']
    except:
        pytest.fail('Did not get access token',  pytrace=False)

    assert len(jwt_token) > 16

    # Store the token for later use
    state.state['base_admin'] = jwt_token


def test_admingetusers(state: State):
    """Verify logged-in base_admin can use JWT to get user list """
    # Build auth string value including token from state
    b_string = 'Bearer ' + state.state['base_admin']

    assert len(b_string) > 24

    auth_hdr = {'Authorization' : b_string}
    response = requests.get(SERVER_URL + "/api/admin/user/get_users", headers=auth_hdr)
    assert response.status_code == 200

    userlist = response.json()
    assert len(userlist) > 1


def test_usergetusers(state: State):
    """Verify logged-in base_user *cannot* use JWT to get user list """
    # Build auth string value including token from state
    b_string = 'Bearer ' + state.state['base_user']

    assert len(b_string) > 24

    auth_hdr = {'Authorization' : b_string}
    response = requests.get(SERVER_URL + "/api/admin/user/get_users", headers=auth_hdr)
    assert response.status_code == 403
