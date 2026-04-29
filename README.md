# ZTrack MongoDB - Integración Intranet FASTAPI-MongoDB

## Docker (recomendado)

### Con Docker Compose (app + MongoDB + MySQL)

```bash
# Construir y levantar todos los servicios
docker compose up -d

# La API estará disponible en http://localhost:8033
# MongoDB en localhost:27017, MySQL en localhost:3306
```

### Solo la aplicación (conectar a bases externas)

```bash
# Crear .env desde el ejemplo
cp .env.example .env
# Editar .env con tus credenciales de MongoDB y MySQL

# Construir y ejecutar
docker build -t ztrack_mongodb .
docker run -p 8033:8033 --env-file .env ztrack_mongodb
```

---

## Instalación manual

*Aspectos del git 
git remote add origin https://github.com/ztrackperu/integrado.git
git branch -M main
git push -u origin maingit

*primero instalar python3.11
*luego establEcer entorno virtual con env de pyhton 
->instalar venv en pyhton (myTest) nombre de entorno virtual
python3 -m venv myTest
->ejecutar entorno virtual en windows
myTest\Scripts\activate
->ejecutar entorno virtual en en linux
source myTest/bin/activate
-> cade vez que haya un archivo con requerimientos se ejecuta de esta manera
pip install -r requirements.txt
-> se requiere crear .env
especificando la conexion a la base de datos
MONGO_DETAILS="mongodb://localhost:27170"
#importante para API con mysql 

pip install mysqlclient
pip install sqlalchemy
pip install pymysql
pip install python-dotenv
#para paginacion
pip install fastapi-pagination

3. pip install sqlalchemy
4. pip install pymysql
pip install requests

pip install mysql-connector-python
#para todo s 
pip install "fastapi[all]"
-> se ejecuta 
python app/main.py

para nivelar permisos en produccion 
alter table permisos add tipo int(11) NOT NULL DEFAULT 1;
alter table permisos add estado int(11) NOT NULL DEFAULT 1;
-> insertar datos basicos
insert into permisos (nombre,tipo) values ("AdminPage",3)("Live",4)