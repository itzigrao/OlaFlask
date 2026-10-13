from app.extensions import db
from flask_login import UserMixin #UserMixin fornece métodos e propriedades que o Flask-Login espera encontrar em um usuário

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
        )

    goals = db.relationship("Goal", back_populates="usuario")