from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)


@app.route("/", methods=["GET"])
def index():
    print('Test')
    return {"status": "Api funcionando"}, 200



