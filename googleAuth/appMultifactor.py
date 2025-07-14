from flask import Flask, request, jsonify#Se importan las librerías para crear la aplicación web y manejar las solicitudes HTTP
from models import db, User#Se importa la instancia de SQLAlchemy y el modelo User
from config import Config#Se importa la configuración de la base de datos
import time#Se importa la librería time para manejar el tiempo de espera en caso de error de conexión a la base de datos
from flask_cors import CORS #Se importa CORS para permitir solicitudes de diferentes orígenes (Cross-Origin Resource Sharing)
from models import Clave2FA#Se importa el modelo Clave2FA para manejar las claves de autenticación de dos factores
from autenticador2Factores import Autenticador2FA#Se importa la clase Autenticador2FA para manejar la autenticación de dos factores

app=Flask(__name__)#Se crea una instancia de Flask para la aplicación web
CORS(app)#Se habilita CORS para la aplicación, permitiendo solicitudes de diferentes orígenes
autenticador=Autenticador2FA()#Se crea una instancia del autenticador de dos factores
app.config.from_object(Config)#Se carga la configuración de la base de datos desde la clase Config
db.init_app(app)#Se inicializa la instancia de SQLAlchemy con la aplicación Flask

@app.route("/obtenerSecreto", methods=["POST"])
def getSecreto():
    datosUsuario=request.get_json()
    #print(datosUsuario, type(datosUsuario))
    claveUsuarioDB=Clave2FA.query.filter_by(userId=datosUsuario["id"]).first()#Se obtiene la clave 2FA del usuario por su ID
    print(claveUsuarioDB, type(claveUsuarioDB))#Se imprime la clave 2FA obtenida de la base de datos
    if claveUsuarioDB.clave is None:
        claveSecreta=autenticador.generarClaveSecreta()#Si no existe, se genera una nueva clave secreta
        uri=autenticador.generarURI(claveSecreta, datosUsuario["username"],"AppProductos")#Se genera una URI para la clave secreta
        claveUsuarioDB.clave=claveSecreta#Se asigna la clave secreta a la clave del usuario
        db.session.commit()#Se confirma la transacción en la base de datos
    else:
        claveSecreta=claveUsuarioDB.clave
        uri=autenticador.generarURI(claveSecreta, datosUsuario["username"],"AppProductos")#Se genera una URI para la clave secreta existente
    
    return jsonify({
        "estado": True,
        "mensaje": "Clave secreta obtenida correctamente",
        "claveSecreta": claveSecreta,
        "uri": uri
    }), 200#Código de estado HTTP 200 indica éxito



@app.route("/actualizarSecreto", methods=["PUT"])
def actualizarSecreto():
    datosUsuario=request.get_json()
    claveUsuarioDB=Clave2FA.query.filter_by(userId=datosUsuario["id"]).first()#Se obtiene la clave 2FA del usuario por su ID
    claveSecreta=autenticador.generarClaveSecreta()#Se genera una nueva clave secreta
    uri=autenticador.generarURI(claveSecreta, datosUsuario["username"],"AppProductos")#Se genera una URI para la clave secreta
    claveUsuarioDB.clave=claveSecreta#Se asigna la nueva clave secreta a la clave del usuario
    db.session.commit()#Se confirma la transacción en la base de datos
    return jsonify({
        "estado": True,
        "mensaje": "Clave secreta actualizada correctamente",
        "claveSecreta": claveSecreta,
        "uri": uri
    }), 200#Código de estado HTTP 200 indica éxito



@app.route("/verificarCodigo", methods=["POST"])
def verificarCodigo():
    datosUsuario=request.get_json()
    #print(datosUsuario, type(datosUsuario))
    codigo=datosUsuario["codigo"]   
    claveUsuarioDB=Clave2FA.query.filter_by(userId=datosUsuario["usuario"]["id"]).first()

    if autenticador.verificarCodigo(codigo, claveUsuarioDB.clave):
        return jsonify({
            "estado": True,
            "mensaje": "Código verificado correctamente"
        }), 200#Código de estado HTTP 200 indica éxito
    else:
        return jsonify({
            "estado": False,
            "mensaje": "Código incorrecto"
        }), 401#Código de estado HTTP 401 indica que la autenticación ha fallado


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

"""SELECT clave,username
FROM "user", clave2_fa
WHERE "user".id = clave2_fa."userId";"""
"""docker exec -it 4-barahonadamian_login_googleauth-db-1 psql -U myuser -d mydatabase"""