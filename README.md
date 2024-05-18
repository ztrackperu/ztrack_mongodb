# incio de proyecto integrado Intranet FASTAPI-MongoDB
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
MONGO_DETAILS="mongodb://localhost:27017"
#importante para API con mysql 

pip install mysqlclient
pip install sqlalchemy
pip install pymysql
pip install python-dotenv

-> se ejecuta 
python app/main.py