from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.db.Column(db.Integer, primary_key=True)
#     email = db.db.Column(db.String(120), unique=True, nullable=False)
#     password = db.db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class Planetas(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(50), nullable=True)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Planetas %r>' % self.name
       
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
        }
    
class Personajes(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(10), nullable=True)
    hair_color = db.Column(db.String(10), nullable=True)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Personajes %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
        }


class Usuarios(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=True)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Usuarios %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
        }
    
class Favoritos(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))

    def __repr__(self):
        return '<Favoritos %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "usuarios_id": self.usuarios_id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id,
        }