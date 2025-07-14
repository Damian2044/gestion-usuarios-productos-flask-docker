from flask_sqlalchemy import SQLAlchemy#Se importa SQLAlchemy para manejar la base de datos

db=SQLAlchemy()#Se crea una instancia de SQLAlchemy

class User(db.Model):#Se crea la clase User que representa la tabla de usuarios en la base de datos
    id=db.Column(db.Integer, primary_key=True)#Se define la columna id como entero y clave primaria
    username=db.Column(db.String(80), unique=True, nullable=False)#Se define la columna username como cadena de texto, única y no nula
    email=db.Column(db.String(120), unique=True, nullable=False)#Se define la columna email como cadena de texto, única y no nula
    password=db.Column(db.String(200), nullable=False)#Se define la columna password como cadena de texto, no nula
    tipoUsuario=db.Column(db.String(50), nullable=False)#Se define la columna tipoUsuario como cadena de texto, no nula
    def __repr__(self):#Método para representar el objeto User como una cadena
        return f'<User {self.username}>'#Representa el objeto User mostrando su nombre de usuario



