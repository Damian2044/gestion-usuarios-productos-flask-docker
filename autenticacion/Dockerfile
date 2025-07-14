#Imagen oficial de Python como base
FROM python:3.9-slim
#Establecer el directorio de trabajo
WORKDIR /appAutenticacion
#Copiar los archivos requeridos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#Copiar el resto de la aplicación
COPY . .
#Exponer el puerto en el que Flask se ejecuta
EXPOSE 5000
# Comando para ejecutar el backend de Autenticación
CMD ["python", "appAutenticacion.py"]
    