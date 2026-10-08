import os

from dotenv import load_dotenv
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "lax"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Usuario(db.Model):
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

@app.route("/register", methods=["POST"])
def register():
    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome:
       return {"Erro": "nome Obrigatório"}, 400
        
    if not email:
        return {"Erro": "email Obrigatório"}, 400
        
    if not senha:
        return {"Erro": "Senha Obrigatório"}, 400

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        return {"Erro": "Email já cadastrado"}, 409

    password_hash=generate_password_hash(senha) 

    usuario = Usuario(
        nome=nome,
        email=email,
        password_hash=password_hash,
    )

        
    try:
        db.session.add(usuario)
        db.session.commit()
        
    except IntegrityError:
        db.session.rollback()
        return {"Erro": "Email já cadastrado"}, 409

    return {"id": usuario.id}, 201

@app.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")


    if not email:
        return {"Erro": "email obrigatório"}, 400

    if not senha:
        return {"Erro": "senha obrigatório"}, 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return {"Erro": "Email ou Senha invalidos"}, 401


    if not check_password_hash(usuario.password_hash, senha):
        return {"Erro": "Email ou Senha invalidos"}, 401

    session["user_id"] = usuario.id

    return {"Status": "Usuario autenticado"}, 200
    


  








