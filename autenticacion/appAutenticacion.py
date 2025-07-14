from flask import Flask, request, jsonify#Se importan las librerías necesarias para crear la aplicación web y manejar las solicitudes HTTP
from config import ConfigAutenticacion#Se importa la configuración de la base de datos para autenticación
from models import db, User#Se importa la instancia de SQLAlchemy y el modelo Usuario
from sqlalchemy import text#Se importa text de SQLAlchemy para ejecutar consultas SQL nativas
import time#Se importa la librería time para manejar pausas en la ejecución
from flask_cors import CORS#Se importa CORS para permitir solicitudes de diferentes orígenes (Cross-Origin Resource Sharing)

app=Flask(__name__)#Se crea una instancia de Flask para la aplicación web
CORS(app)#Se habilita CORS para la aplicación, permitiendo solicitudes de diferentes orígenes
app.config.from_object(ConfigAutenticacion)#Se carga la configuración de la base de datos desde la clase ConfigAutenticacion
db.init_app(app)
def validarConexionConsulta(usuario,password,intentos=1,espera=1):
    for intento in range(intentos):
        try:
            with app.app_context():
                user=User.query.filter_by(username=usuario, password=password).first()
                print("Conexión a la base de datos exitosa...!")
            return (True, user)#conexión OK y resultado (objeto o None)
        except Exception as error:
            print(f"Error en la conexión a la base de datos, intento={intento+1},{error}...!")
            time.sleep(espera)
    return (False, None)




@app.route("/apiLogin", methods=["POST"])
def login():
    datosUsuario=request.get_json()
    print(datosUsuario,type(datosUsuario))
    usuario=datosUsuario["username"]
    password=datosUsuario["password"]
  
    conexion,UserAutenticado=validarConexionConsulta(usuario,password)
    if not conexion:
        return jsonify({"estado": False, "mensaje": "Error en la conexión a la base de datos"}), 500
    

    print(UserAutenticado,type(UserAutenticado))
    if UserAutenticado:
        return jsonify({"estado": True, "mensaje": "Usuario autenticado correctamente",
                        "usuario": {
                            "id": UserAutenticado.id,
                            "username": UserAutenticado.username,
                            "email": UserAutenticado.email,
                            "tipoUsuario": UserAutenticado.tipoUsuario
        }}), 200
    else:
        return jsonify({"estado": False, "mensaje": "Usuario o contraseña incorrectos"}), 401


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)