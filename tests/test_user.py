from unittest import mock
from unittest.mock import patch
from tests.conftest import app, client
import json
import jwt
from flask import current_app
from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User


def test_create_admin_user(client, db):
    
    # Test create admin user with no SuperAdmin user already exists
    response = client.post('/admin')
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'SuperAdmin created'}

    # Test create admin user when SuperAdmin already exists
    response = client.post('/admin')
    assert response.status_code == 409
    assert json.loads(response.data) == {'message': 'SuperAdmin already exists'}

    # Verify that SuperAdmin user has been added to the database
    assert db.session.query(User).filter_by(username='SuperAdmin').first() is not None


"""

def test_login(client, db, mock_user):
    # Ajout du mock_user à la base de données pour le test de connexion
    db.session.add(mock_user)
    db.session.commit()




    # Test avec des identifiants corrects
    response = client.get('/login', headers={'Authorization': 'Basic ' + b64encode(b'mockuser:123456').decode()})
    assert response.status_code == 200
    assert 'token' in response.json

    # Test avec un mauvais nom d'utilisateur
    response = client.get('/login', headers={'Authorization': 'Basic ' + b64encode(b'wrong_user:password').decode()})
    assert response.status_code == 401
    assert 'Could not verify' in response.get_data(as_text=True)

    # Test avec un mauvais mot de passe
    response = client.get('/login', headers={'Authorization': 'Basic ' + b64encode(b'mockuser:wrong_password').decode()})
    assert response.status_code == 401
    assert 'Could not verify' in response.get_data(as_text=True)

    # Suppression du mock_user de la base de données après le test
    db.session.delete(mock_user)
    db.session.commit()

"""


