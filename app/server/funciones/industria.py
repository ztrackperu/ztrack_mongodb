import json
import mysql.connector
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from server.generico.base_conexion import BaseConexion
#from dateutil.relativedelta import relativedelta

baseD = "ZTRACK_INDUSTRIA"
databaseMongo = client[baseD]

def bd_gene(imei):
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    part = fet.strftime('_%m_%Y')
    colect ="D_"+imei+part
    return colect

def procesar_fecha(fechaI="0",fechaF="0"):
    fecha_hoy =datetime.now()
    if(fechaF=="0"):
        fechaIx=  fecha_hoy-timedelta(hours=12)
        fechaFx = fecha_hoy
    else:
        fechaIx=  datetime.fromisoformat(fechaI)
        fechaFx = datetime.fromisoformat(fechaF)
    data = [fechaIx,fechaFx]
    return data


async def data_industria_grafica(notificacion_data: dict) -> dict:
    print(notificacion_data['imei'])
    coleccion_principal = bd_gene(notificacion_data['imei'])
    madurador = databaseMongo.get_collection(coleccion_principal)
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fech = procesar_fecha()
    else : 
        fech = procesar_fecha(notificacion_data['fechaI'],notificacion_data['fechaF'])    
    diferencial =[{"IMEI":notificacion_data['imei'] ,"fecha_recepcion": {"$gte": fech[0],"$lte": fech[1]}}]
    pip = [{"$match": {"$and":diferencial}},  {"$sort": {"fecha_recepcion": -1}}] 
    humidity =[]
    temperature=[]
    EC =[]
    PH =[]
    N =[]
    P =[]
    K =[]
    power =[]
    fechas=[]
    async for concepto_ot in madurador.aggregate(pip):
        fechas.append(concepto_ot['fecha_recepcion'])
        humidity.append(concepto_ot['humidity'])
        temperature.append(concepto_ot['temperature'])
        EC.append(concepto_ot['EC'])
        PH.append(concepto_ot['PH'])
        N.append(concepto_ot['N'])
        P.append(concepto_ot['P'])
        K.append(concepto_ot['K'])
        power.append(concepto_ot['power'])
    final = {
        "IMEI" :notificacion_data['imei'],
        "humidity":humidity,
        "temperature":temperature,
        "EC":EC,
        "PH":PH,
        "N":N,
        "P":P,
        "K":K,
        "power":power,
        "fecha":fechas
    }
    return final

async def data_industria_tabla(notificacion_data: dict) -> dict:
    print(notificacion_data['imei'])
    coleccion_principal = bd_gene(notificacion_data['imei'])
    madurador = databaseMongo.get_collection(coleccion_principal)
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fech = procesar_fecha()
    else : 
        fech = procesar_fecha(notificacion_data['fechaI'],notificacion_data['fechaF'])   
    diferencial =[{"IMEI":notificacion_data['imei'] ,"fecha_recepcion": {"$gte": fech[0],"$lte": fech[1]}}]
    pip = [{"$match": {"$and":diferencial}},  
              {"$sort": {"fecha_recepcion": -1}},{"$project":{"_id": 0,"id":0,"IMEI":0}}]
    tabla =[]
    async for concepto_ot in madurador.aggregate(pip):
        tabla.append(concepto_ot)
    final = {
        "IMEI" :notificacion_data['imei'],
        "datos":tabla
    }
    return final

