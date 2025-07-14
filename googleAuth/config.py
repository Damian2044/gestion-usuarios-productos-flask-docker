import os#Se importa la librería os para manejar variables de entorno

class Config:#Clase que tiene la configuración para Flask usando SQLAlchemy
    #URI de la base de datos postgresql, se obtiene de una variable de entorno o valor por defecto
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') or 'postgresql://myuser:mypassword@db:5432/mydatabase'
    SQLALCHEMY_TRACK_MODIFICATIONS=False#Desactiva el seguimiento de modificaciones en los objetos del modelo de la base de datos
