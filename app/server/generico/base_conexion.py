from server.generico.base_mysql import db_connection_mysql
from datetime import datetime

class BaseConexion :

    def __init__(self):
        self.config = db_connection_mysql
        #self.session = self.orm_config.session 
        #self.session = self.orm_config.session

    def obtener_mes_y_anio_actual():
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.month
        anio_actual = fecha_actual.year
        mes_anio_str = f"{mes_actual}_{anio_actual}"
        return mes_anio_str
    
    
    

