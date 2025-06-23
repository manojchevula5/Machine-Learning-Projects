import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import io
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Disease' in response.data  # Check for expected content

def test_upload_page_get(client):
    response = client.get('/uimg')
    assert response.status_code == 200
    assert b'Upload' in response.data or b'file' in response.data

def test_upload_page_post_invalid(client):
    data = {'file': (io.BytesIO(b"fake image data"), 'test.txt')}
    response = client.post('/uimg', data=data, content_type='multipart/form-data')
    assert response.status_code == 200 or response.status_code == 500

def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
