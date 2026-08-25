

from app import app, db

def test_register_usuario():
    client =  app.test_client()

    response = client.post(
        "/register",
        json={
            "nome": "ana",
            "email": "teste@gmail.com",
            "senha": "Banana232"
        }
    )

    assert response.status_code == 201