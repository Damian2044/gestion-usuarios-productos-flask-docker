from flask_sqlalchemy import SQLAlchemy# Se importa SQLAlchemy para manejar la base de datos
db=SQLAlchemy()#Se crea una instancia de SQLAlchemy

class Producto(db.Model):#Se crea la clase Producto que representa la tabla de productos en la base de datos
    id=db.Column(db.Integer, primary_key=True)#Se define la columna id como entero y clave primaria
    nombre=db.Column(db.String(80), unique=True, nullable=False)#Se define la columna nombre como cadena de texto, única y no nula
    precio=db.Column(db.Float, nullable=False)#Se define la columna precio como flotante y no nula 

    def __repr__(self):#Método para representar el objeto Producto como una cadena
        return f'<Producto {self.nombre}>'



