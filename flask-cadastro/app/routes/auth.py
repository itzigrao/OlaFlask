from flask import Blueprint, request, render_template
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import(
    generate_password_hash,
    check_password_hash,
)

from app.extensions import db
from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)#cria um objeto que administra um conjunto de rotas

@auth_bp.route("/register", methods=['GET','POST'])
def register():

    if request.method == 'GET':
        return render_template('registro.html')


    elif request.method == 'POST':
        dados = request.get_json(silent=True) or {}

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

    
        return {
            "id": usuario.id,
            "mensagem": "Usuário cadastrado",
            "redirect": "/login",
            }, 201

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    
    
    elif request.method == 'POST':

        dados = request.get_json(silent=True) or {}

        email = dados.get("email")
        senha = dados.get("senha")


        if not email:
            return {"Erro": "Email obrigatório"}, 400

        if not senha:
            return {"Erro": "Senha obrigatória"}, 400

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return {"Erro": "Email ou Senha invalidos"}, 401


        if not check_password_hash(usuario.password_hash, senha):
            return {"Erro": "Email ou Senha invalidos"}, 401

        login_user(usuario)

        

        return {
            "id": usuario.id,
            "mensagem": "Login realizado com sucesso!",
            "redirect": "/home"
            }, 200

@auth_bp.route('/logout', methods=["POST"])
@login_required
def logout ():
    logout_user()
    
    return {"mensagem": "Logout realizado com sucesso",
            "redirect": "/login"}, 200




