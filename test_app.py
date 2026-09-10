import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Catalogue' in response.data or b'ShopDemo' in response.data


def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_cart_empty_by_default(client):
    response = client.get('/cart')
    assert response.status_code == 200
    assert 'panier est vide'.encode('utf-8') in response.data
