import pytest
from unittest.mock import patch
from app import app, db, Job

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_fetch_jobs(client):
    mock_data = [{'title': 'Software Engineer', 'company': 'Tech Corp', 'location': 'NYC'}]
    
    with patch('requests.get') as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = mock_data
        
        response = client.post('/', data={'keyword': 'engineer'})
        
        assert b'Software Engineer' in response.data

        with app.app_context():
            assert Job.query.count() == 1
