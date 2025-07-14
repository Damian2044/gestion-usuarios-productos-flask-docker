from flask import Flask, request, jsonify# Se importan las librerías necesarias para crear la aplicación web y manejar las solicitudes HTTP
from models import db, Producto#Se importa la instancia de SQLAlchemy y el modelo Producto
from config import ConfigProductos#Se importa la configuración de la base de datos para productos 
import time
from flask_cors import CORS #Se importa CORS para permitir solicitudes de diferentes orígenes (Cross-Origin Resource Sharing)
app=Flask(__name__)#Se crea una instancia de Flask para la aplicación web
CORS(app) 
app.config.from_object(ConfigProductos)#Se carga la configuración de la base de datos desde la clase ConfigProductos
db.init_app(app)#Se inicializa la instancia de SQLAlchemy con la aplicación Flask

with app.app_context():# Se crea un contexto de aplicación para poder interactuar con la base de datos
    while True:
        try:
            db.create_all()# Se crea la tabla definida en el modelo Producto
            print("Conexión a la base de datos exitosa...!")
            break
        except Exception as error:
            print(f"Error en la conexión a la base de datos: {error}...!")
            time.sleep(5)


@app.route('/productos', methods=['POST'])# Se define la ruta para crear un nuevo producto
def create_producto():
    data=request.get_json()#Obtiene los datos del producto desde la solicitud JSON
    new_producto=Producto(nombre=data['nombre'], precio=data['precio'])#Crea una nueva instancia de Producto
    db.session.add(new_producto)#Añade el nuevo producto a la base de datos
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'Producto created successfully'}), 201#Devuelve un mensaje de éxito y el código de estado 201

@app.route('/productos', methods=['GET'])#Se define la ruta para obtener todos los productos
def get_productos():
    productos=Producto.query.all()#Obtiene todos los productos de la base de datos
    return jsonify([{'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio} for producto in productos])

@app.route('/productos/<int:id>', methods=['GET'])#Se define la ruta para obtener un producto específico por su ID
def get_producto(id):
    producto = Producto.query.get_or_404(id)#Obtiene un producto por su ID o devuelve un error 404 si no se encuentra
    return jsonify({'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio})

@app.route('/productos/<int:id>', methods=['PUT'])#Se define la ruta para actualizar un producto específico por su ID
def update_producto(id):
    data=request.get_json()#Obtiene los datos del producto desde la solicitud JSON
    producto=Producto.query.get_or_404(id)#Obtiene un producto por su ID o devuelve un error 404 si no se encuentra
    producto.nombre=data['nombre']
    producto.precio=data['precio']
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'Producto updated successfully'})

@app.route('/productos/<int:id>', methods=['DELETE'])#Se define la ruta para eliminar un producto específico por su ID
def delete_producto(id):
    producto=Producto.query.get_or_404(id)#Obtiene un producto por su ID o devuelve un error 404 si no se encuentra
    db.session.delete(producto)#Elimina el producto de la base de datos
    db.session.commit()#Confirma los cambios en la base de datos
    return jsonify({'message': 'Producto deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)# Se inicia la aplicación Flask en el puerto 5000
