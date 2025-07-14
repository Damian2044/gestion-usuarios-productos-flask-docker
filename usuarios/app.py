from flask import Flask, request, jsonify#Se importan las librerías para crear la aplicación web y manejar las solicitudes HTTP
from models import db, User#Se importa la instancia de SQLAlchemy y el modelo User
from config import Config#Se importa la configuración de la base de datos
import time#Se importa la librería time para manejar el tiempo de espera en caso de error de conexión a la base de datos
from flask_cors import CORS #Se importa CORS para permitir solicitudes de diferentes orígenes (Cross-Origin Resource Sharing)
from models import Clave2FA#Se importa el modelo Clave2FA para manejar las claves de autenticación de dos factores

app=Flask(__name__)#Se crea una instancia de Flask para la aplicación web
CORS(app) #Se habilita CORS para la aplicación Flask, permitiendo solicitudes de diferentes orígenes
app.config.from_object(Config)#Se carga la configuración de la base de datos desde la clase Config
db.init_app(app)#Se inicializa la instancia de SQLAlchemy con la aplicación Flask

with app.app_context():#Se crea un contexto de aplicación para poder interactuar con la base de datos
    while True:
        try:
            db.create_all()#Se crea la tabla definida en el modelo
            print("Conexión a la base de datos exitosa...!")
            #Crear un usuario administrador por defecto si no existe
            if not User.query.filter_by(username='admin').first():#Verifica si ya existe un usuario con el nombre de usuario 'admin'
                admin=User(username='admin',email='admin@ejemplo.com', password='admin123', tipoUsuario='administrador')#Crea un nuevo usuario administrador
                db.session.add(admin)#Añade el nuevo usuario administrador a la sesión de la base de datos
                db.session.commit()#Confirma los cambios en la base de datos
                claveAdmin=Clave2FA(userId=admin.id, clave=None)#Crea una nueva clave 2FA para el usuario administrador
                db.session.add(claveAdmin)#Añade la nueva clave 2FA a la sesión de la base de datos
                db.session.commit()#Confirma los cambios en la base de datos
                print("Usuario administrador creado con éxito...!")
            else:
                print("El usuario administrador ya existe...!")
            break
        except Exception as error:
            print(f"Error en la conexión a la base de datos: {error}...!")
            time.sleep(5)


@app.route('/users', methods=['POST'])#Se define la ruta para crear un nuevo usuario
def create_user():
    data=request.get_json()#Obtiene los datos del usuario desde la solicitud JSON
    new_user=User(username=data['username'], email=data['email'], password=data['password'],tipoUsuario=data['tipoUsuario'])#Crea una nueva instancia de User 
    db.session.add(new_user)#Añade el nuevo usuario a la base de datos
    db.session.commit()#Confirma los cambios en la base de datos
    clave2fa=Clave2FA(userId=new_user.id, clave=None)#Crea una nueva instancia de Clave2FA para el nuevo usuario
    db.session.add(clave2fa)#Añade la nueva clave 2FA a la base de datos
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'User created successfully'}), 201#Devuelve un mensaje de éxito y el código de estado 201 

@app.route('/users', methods=['GET'])#Se define la ruta para obtener todos los usuarios
def get_users():
    users=User.query.all()#Obtiene todos los usuarios de la base de datos
    return jsonify([{'id': user.id, 'username': user.username, 
                     'email': user.email, 'password': user.password,'tipoUsuario':user.tipoUsuario} for user in users])

@app.route('/users/<int:id>', methods=['GET'])#Se define la ruta para obtener un usuario específico por su ID
def get_user(id):
    user=User.query.get_or_404(id)#Obtiene un usuario por su ID o devuelve un error 404 si no se encuentra
    return jsonify({'id': user.id, 'username': user.username, 
                    'email': user.email, 'password': user.password,'tipoUsuario':user.tipoUsuario})

@app.route('/users/<int:id>', methods=['PUT'])#Se define la ruta para actualizar un usuario específico por su ID
def update_user(id):
    data=request.get_json()#Obtiene los datos del usuario desde la solicitud JSON
    user=User.query.get_or_404(id)#Obtiene un usuario por su ID o devuelve un error 404 si no se encuentra
    user.username=data['username']
    user.email=data['email']
    user.password=data['password']
    user.tipoUsuario=data['tipoUsuario']
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:id>', methods=['DELETE'])#Se define la ruta para eliminar un usuario específico por su ID
def delete_user(id):
    user=User.query.get_or_404(id)#Obtiene un usuario por su ID o devuelve un error 404 si no se encuentra
    db.session.delete(user)#Elimina el usuario de la base de datos
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)#Se inicia la aplicación Flask en el puerto 5000
