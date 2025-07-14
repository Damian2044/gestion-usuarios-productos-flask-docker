from flask_sqlalchemy import SQLAlchemy#Se importa SQLAlchemy para manejar la base de datos

db=SQLAlchemy()#Se crea una instancia de SQLAlchemy

class User(db.Model):#Se crea la clase User que representa la tabla de usuarios en la base de datos
    id=db.Column(db.Integer, primary_key=True)#Se define la columna id como entero y clave primaria
    username=db.Column(db.String(80), unique=True, nullable=False)#Se define la columna username como cadena de texto, única y no nula
    email=db.Column(db.String(120), unique=True, nullable=False)#Se define la columna email como cadena de texto, única y no nula
    password=db.Column(db.String(200), nullable=False)#Se define la columna password como cadena de texto, no nula
    tipoUsuario=db.Column(db.String(50), nullable=False)#Se define la columna tipoUsuario como cadena de texto, no nula
    #Relación
    relacionClave2FA=db.relationship('Clave2FA',#Se establece una relación con la clase Clave2FA
                                     backref='usuario',#Permite acceder desde Clave2FA al usuario con: clave.usuario
                                     uselist=False,#Indica que es una relación uno a uno (no lista)
                                     cascade='all, delete',#Se define el comportamiento de cascada para eliminar claves 2FA al eliminar un usuario 
                                     passive_deletes=True)#Delega a la base de datos la eliminación en cascada (si `ondelete='CASCADE'` está en la FK)
    
    
    
    def __repr__(self):#Método para representar el objeto User como una cadena
        return f'<User {self.username}>'#Representa el objeto User mostrando su nombre de usuario



class Clave2FA(db.Model):#Se crea la clase Clave2FA que representa la tabla de claves 2FA en la base de datos
    id=db.Column(db.Integer, primary_key=True)#Se define la columna id como entero, clave primaria
    userId=db.Column(db.Integer,#Se define la columna userId como entero, 
                     db.ForeignKey('user.id',#Referencia a la clave primaria de la tabla User
                                   ondelete='CASCADE'),#Elimina la clave 2FA si el usuario es eliminado 
                                   nullable=False,#No nula
                                   unique=True)#Clave foránea que referencia a la tabla User única
    clave=db.Column(db.String(200))#Se define la columna clave como cadena de texto, no nula


    def __repr__(self):#Método para representar el objeto Clave2FA como una cadena
        return f'<Clave2FA {self.clave}>'#Representa el objeto Clave2FA mostrando su clave
