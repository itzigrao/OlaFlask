from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import(
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)#cria um objeto que administra um conjunto de rotas

@auth_bp.route("/register", methods=['GET','POST'])
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

@auth_bp.route("/login", methods=["POST"])
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

