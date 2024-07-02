# Comience desde la imagen base oficial de Python.
FROM python:3.12.4

# Establezca el directorio de trabajo actual en /code.
#Aquí es donde colocaremos el archivo requisitos.txt y el directorio de la aplicación.
#WORKDIR /code
WORKDIR /ztrack_mongodb
# Copie el archivo con los requisitos al directorio /code.
#Copie primero solo el archivo con los requisitos, no el resto del código.
#Como este archivo no cambia con frecuencia, Docker lo detectará y utilizará el caché para este paso, habilitando el caché también para el siguiente paso.

#COPY ./requirements.txt /code/requirements.txt
COPY ./requirements.txt /ztrack_mongodb/requirements.txt

#Instale las dependencias del paquete en el archivo de requisitos.
#La opción --no-cache-dir le dice a pip que no guarde los paquetes descargados localmente, ya que eso es solo si pip se va a ejecutar nuevamente para instalar los mismos paquetes, pero ese no es el caso cuando se trabaja con contenedores.
#La opción --upgrade le dice a pip que actualice los paquetes si ya están instalados.
#Debido a que la caché de Docker podría detectar el paso anterior al copiar el archivo, este paso también utilizará la caché de Docker cuando esté disponible.
#Usar el caché en este paso le ahorrará mucho tiempo al crear la imagen una y otra vez durante el desarrollo, en lugar de descargar e instalar todas las dependencias cada vez
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ztrack_mongodb/requirements.txt


# Como esto tiene todo el código que es lo que cambia con más frecuencia la caché de Docker no se utilizará para este o cualquiera de los siguientes pasos fácilmente.
#Por lo tanto, es importante poner esto cerca del final del Dockerfile, para optimizar los tiempos de construcción de la imagen del contenedor.
#COPY ./app /code/app
COPY ./app /ztrack_mongodb/app


#Configura el comando para usar fastapi run, que usa Uvicorn por debajo.
#CMD toma una lista de cadenas, cada una de estas cadenas es lo que usted escribiría en la línea de comandos separadas por espacios.
#Este comando se ejecutará desde el directorio de trabajo actual, el mismo directorio /code que estableció anteriormente con WORKDIR /code. 
CMD ["fastapi", "run", "app/main.py", "--port", "8033"]