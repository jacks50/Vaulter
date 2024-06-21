import pytest
from vaulter import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_vaulter_filecreate(client):
    # page is available
    assert client.get('/vaulture/file/create').status_code == 200

    # must create a file in the vault_storage directory
    response = client.post('/vaulture/file/create', data={'filename': 'annoying_testing_666'})
    assert response.status_code == 200

    # filename must be unique

    # file must be empty

    # file naming convention is "name_from_constants_[token_id]"

    # file is returned to user with : filename = name_from_constants / token_id = token_id

    return True

def test_vaulter_fileget(client):
    # must specify a filename

    # must specify a token_id

    # filename must exist on vault_storage directory with token

    # file is returned to user

    return True

def test_vaulter_fileupload(client):
    # file must not be empty

    # file must not exceed 16MB

    # filename must be specified

    # filename must be unique

    # filename is saved with a token that doesn't exist

    # token must be returned

    return True

def test_vaulter_fileupdate(client):
    # file must not be empty

    # file must not exceed 16MB

    # filename and token_id must be specified

    # file is updated in vault_storage

    return True

def test_vaulter_filelist(client):
    # admin password must be provided

    # listing only shows files without tokens

    return True