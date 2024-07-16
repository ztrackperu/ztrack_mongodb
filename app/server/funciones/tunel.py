import json
#import mysql.connector
from server.database import client
from bson import regex
from datetime import datetime,timedelta

def per_actual():
    now = datetime.now()
    mes = now.month 
    per = now.year
    periodo = str(mes)+"_"+str(per)
    return periodo

async def data_hortifruit(notificacion_data: dict) -> dict:
    #capturar hora 
    #desglozar la data y almacenar en base de datos REPOSITORIO_MES_AÑO
    palm = "HORTIFRUIT_"+per_actual()
    database = client[palm]
    cadenaWonderful = notificacion_data['data']
    listaWonderful = cadenaWonderful.split(",")
    device = listaWonderful[3]
    #deviceW = device.split("|")
    #deviceW1 =deviceW[0]

    tunel = database.get_collection(device)
    #tunel = database.get_collection(deviceW1)
    fet =datetime.now()
    notificacion_data['fecha'] = fet
    print(notificacion_data)
    notificacion = await tunel.insert_one(notificacion_data)
    new_notificacion = await tunel.find_one({"_id": notificacion.inserted_id},{"_id":0})
    #return notificacion_helper(new_notificacion)
    print(palm)
    return new_notificacion