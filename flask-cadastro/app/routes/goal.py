from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError


from app.extensions import db
from app.models import Goal


goal_bp = Blueprint("goal", __name__)



@goal_bp.route("/create_goal", methods=['GET', 'POST'])
@login_required
def create_goal():

    if request.method == 'GET':
        return render_template('crud.html')

    elif request.method == 'POST':

        dados = request.get_json(silent=True) or {}

        titulo = dados.get("titulo")
        descricao = dados.get("descricao")

        if titulo is not None:
            titulo = titulo.strip()

        if not titulo:
            return {"Erro": "Título obrigatório"}, 400

        goal_existente = Goal.query.filter_by(titulo=titulo, usuario_id=current_user.id).first()

        if goal_existente:
            return {"Erro": "Objetivo já existe"}, 409


        novo_goal = Goal(
            titulo=titulo,
            descricao=descricao,
            usuario_id=current_user.id
        )

        try:
            db.session.add(novo_goal)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            return {"Erro": "Operacional. Tente novamente mais tarde"}, 409

        return {
            "goal_id": novo_goal.id,
            "mensagem": "Objetivo cadastrado",
            "redirect": "/crud"
        }, 201


@goal_bp.route('/list_goal', methods=['GET'])
@login_required
def list_goal():

    goals = current_user.goals

    lista_goal = []

    for goal in goals:
        lista_goal.append({
            "id": goal.id,
            "titulo": goal.titulo,
            "descricao": goal.descricao
        })

    if lista_goal is None:
        return {
            "usuario_id": current_user.id,
            "lista": lista_goal,
            "Erro": "Lista sem objetivos",
            "redirect": "/create_goal"
            }, 400


    return {
        "usuario_id": current_user.id,
        "lista": lista_goal,
        "mensagem": "Vizualização de lista de objetivos OK",
    },200

# jsonify(lista_goal), 201


@goal_bp.route('/update_goal/<int:goal_id>', methods=['PATCH'])
@login_required
def update_goal(goal_id):

    goal = Goal.query.filter_by(
        id = goal_id,
        usuario_id = current_user.id
    ).first()

    if goal is None:
        return {"Erro": "Objetivo não encontrado"}, 404

    dados = request.get_json(silent=True) or {}

    novo_titulo = dados.get('titulo')
    nova_descricao = dados.get('descricao')

    if novo_titulo is not None:
        novo_titulo = novo_titulo.strip()

    if not novo_titulo:
        return {"Erro": "Título obrigatório"}, 400


    goal_existente = Goal.query.filter(
        Goal.titulo == novo_titulo,
        Goal.usuario_id == current_user.id,
        Goal.id != goal_id
        ).first()
    
    if goal_existente:
        return {"Erro": "objetivo já existe"}, 409

    goal.titulo = novo_titulo

    if nova_descricao is not None:
        goal.descricao = nova_descricao.strip()

    try:

        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return{'Erro': 'Não foi possivel atualizar o objetivo!'}, 409

    return {
        "id": goal.id,
        "titulo": goal.titulo,
        "descricao": goal.descricao,
        "mensagem": "Objetivo atualizado com sucesso"
    }, 200

@goal_bp.route('/delete_goal/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal (goal_id):

    goal = Goal.query.filter_by(
        id = goal_id,
        usuario = current_user
    ).first()

    if goal is None:
        return {"Erro":"Objetivo selecionado não existe"}, 404

    try:
        db.session.delete(goal)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"Erro": "Erro inesperado. Tente novamente mais tarde."}, 409

    return {
        "goal_id": goal.id,
        "mensagem": "Objetivo deletado com sucesso",
        "redirect": "/list_goal"
    }


@goal_bp.route("/crud")
@login_required
def crud():
    return render_template("crud.html")



    
    


    





    



        
            


        


    

