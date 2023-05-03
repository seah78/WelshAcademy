import json
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
