import json
from server.database import client
from bson import regex

async def data_madurador(notificacion_data: dict) -> dict:
    #pedir la ultima conexion 
    #ultima conexion pedir mes y año 
                                                                                                                                                                         
    #construir base de datos 
    #database = client.intranet
    per = notificacion_data['ultima'].split('T')
    #ARRAY 0 represnta la fecha y 1 la hora
    periodo = per[0].split('-')
    #periodo 0 , es el año , 1 es el mes , 2 es el dia 
    #armamos la base de datos 
    bd = notificacion_data['device']+"_"+str(int(periodo[1]))+"_"+periodo[0]
    database = client[bd]
    print(bd)
    madurador = database.get_collection("madurador")
    #notificacion_collection = collection("notificaciones")
    notificacions = []                                          
    async for mad in madurador.find({},{"_id":0}).limit(30):
        print(mad)
        notificacions.append(mad)
    return notificacions



#async def add_notificacion(notificacion_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    #notificacion = await notificacion_collection.insert_one(notificacion_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    #new_notificacion = await notificacion_collection.find_one({"_id": notificacion.inserted_id})
    #return notificacion_helper(new_notificacion)                             