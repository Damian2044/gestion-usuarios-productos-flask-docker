import os#Se importa la librería os para manejar variables de entorno

class ConfigAutenticacion:#Clase que tiene la configuración para Flask usando SQLAlchemy
    #URI de la base de datos postgresql, se obtiene de una variable de entorno o valor por defecto
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_USUARIOS') or 'postgresql://myuser:mypassword@127.0.0.1:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS=False#Desactiva el seguimiento de modificaciones en los objetos del modelo de la base de datos
