"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planetas, Personajes, Usuarios, Favoritos
#from models import Person
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    todoslospersonajes = Personajes.query.all()
    if todoslospersonajes == [] :
        return jsonify({"msg":"No se encuentran personajes"})
    resultado = list(map(lambda personaje:personaje.serialize(),todoslospersonajes))
    return jsonify(resultado),200

@app.route('/personajes', methods=['POST'])
def post_personajes():
    body = json.loads(request.data)
    new_personaje = Personajes.query.filter_by(name=body["name"]).first() 
    if new_personaje is None: 
        new_personaje = Personajes(
            name = body["name"],
            eye_color = body["eye_color"],
            hair_color = body["hair_color"],

        )
        db.session.add(new_personaje)
        db.session.commit()
        return jsonify({"msg": "personaje creado"})
    return jsonify({"msg": "personaje NO creado"})

@app.route('/planetas', methods=['GET'])
def get_planetas():
    todoslosplanetas = Planetas.query.all()
    if todoslosplanetas == [] :
        return jsonify({"msg":"No se encuentran planetas"})
    resultado = list(map(lambda planeta:planeta.serialize(),todoslosplanetas))
    return jsonify(resultado),200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    todoslosusuarios = Usuarios.query.all()
    if todoslosusuarios == [] :
        return jsonify({"msg":"No se encuentran usuarios"})
    resultado = list(map(lambda usuario:usuario.serialize(),todoslosusuarios))
    return jsonify(resultado),200

@app.route('/favoritos', methods=['GET'])
def get_favoritos():
    todoslosfavoritos = Favoritos.query.all()
    if todoslosfavoritos == [] :
        return jsonify({"msg":"No se encuentran favoritos"})
    resultado = list(map(lambda favorito:favorito.serialize(),todoslosfavoritos))
    return jsonify(resultado),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
