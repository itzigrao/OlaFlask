from conftest import app, client

def test_register_usuario(client):
    response = client.post(
        "/register",
        json={
            "nome": "ana",
            "email": "teste@gmail.com",
            "senha": "Banana232"
        }
    )

    assert response.status_code == 201

    dados = response.get_json()

    assert "id" in dados


def test_register_sem_senha(client):
    response = client.post(
        "/register",
        json={
            "nome": "Carlos",
            "email": "carlos@gmail.com"
        }

    )

    assert response.status_code == 400


def test_register_email_duplicado(client):

    dados={
            "nome": "ana",
            "email": "teste@gmail.com",
            "senha": "Banana232"
        }
    

    primeira = client.post("/register", json=dados)
    segunda = client.post("/register", json=dados)

    assert primeira.status_code == 201
    assert segunda.status_code ==409



