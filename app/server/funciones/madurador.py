import json
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from fastapi_pagination.ext.motor import paginate


# import all you need from fastapi-pagination

async def config(empresa :int):
    notificacions=[]
    database =client["config_ztrack"]
    empresa_config= database.get_collection("empresa_config")
    async for mad in empresa_config.find({"user_id":empresa},{"_id":0}):
        notificacions.append(mad)
    #se debe extraer el primir resultado
    return notificacions[0]

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
    #print(bd)
    #print("olitas")
    #print(notificacion_data['empresa'])
    #print(notificacion_data['page'])
    #print(notificacion_data['size'])
    madurador = database.get_collection("madurador")
    #notificacion_collection = collection("notificaciones")
    page=notificacion_data['page']
    limit=notificacion_data['size']
    empresa =notificacion_data['empresa']
    #esquema para consultar data 
    dataConfig =await config(empresa)
    #print(dataConfig)
    #print(dataConfig['config_data'])
    #print(dataConfig['config_graph'])
    #result = madurador.find({ "$and": [{"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},{"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}]},{"_id":0})                                
    #esquema con agregation para mayor versatilidad
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fechaI = datetime.fromisoformat(notificacion_data['ultima'])
        one_day = timedelta(hours=12)
        fecahF = fechaI-one_day
        #print(certeza)
        #print(certeza1)
    else : 
        fechaI=datetime.fromisoformat(notificacion_data['fechaI'])
        fecahF=datetime.fromisoformat(notificacion_data['fechaF'])
    pip = [
        {"$match": 
            {"created_at": {"$gte": fechaI },
            "created_at": {"$lte": fecahF}}},  
        {"$project":dataConfig['config_data']},
        {"$skip" : (page-1)*limit},
        {"$limit" : limit},  
    ]

    #recorrer array y crear varaibles para insertar
    graph = dataConfig['config_graph']
    #print("baja")
    #print(graph)
    #print("alta")
    listas = {}
    for i in range(len(graph)):
        nombre_lista = f"{graph[i]}"
        listas[nombre_lista] = []

    concepto_ots = []
    async for concepto_ot in madurador.aggregate(pip):
        #print(concepto_ot)
        concepto_ots.append(concepto_ot)
        for i in range(len(graph)):
           #dataConfig['config_graph'][i].append(concepto_ot[dataConfig['config_graph'][i]])
           dato =graph
           #print(dato)
           listas[dato[i]].append(concepto_ot[dato[i]])
           #print(concepto_ot[dato[i]])
           #dato[i].append(concepto_ot[dato[i]])
        #print(concepto_ot['return_air'])
    #print(listas)
    listasT = {"graph":listas,"table":concepto_ots}
    #print(listasT)

    return listasT




#async def add_notificacion(notificacion_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    #notificacion = await notificacion_collection.insert_one(notificacion_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    #new_notificacion = await notificacion_collection.find_one({"_id": notificacion.inserted_id})
    #return notificacion_helper(new_notificacion)   

                        
async def obtener_madurador() -> dict:
    bd = "ZGRU9015808_5_2024"
    database = client[bd]
    print(bd)
    madurador = database.get_collection("madurador")
    notificacions = []
    pip = [
            { 
                "$and": [
                    {"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},
                    {"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}
                    ]
            },
            {"_id":0}
        ]  
    async for mad in madurador.find({ "$and": [{"created_at": {"$gte": datetime.fromisoformat("2024-05-07T00:00:00.000Z")}},{"created_at": {"$lte": datetime.fromisoformat("2024-05-09T23:59:59.999Z")}}]},{"_id":0}):
        notificacions.append(mad)
    return  notificacions

