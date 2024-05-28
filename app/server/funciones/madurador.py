import json
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from fastapi_pagination.ext.motor import paginate

datosDepurar = [
    32752,-32752, 3275.2, -3275.2, 327.52,-327.52, 32767, -32767, 3276.7, -3276.7, 327.67, -327.67,32766, -32766 , 3276.6, -3276.6, 327.66, -327.66,
    32765, -32765, 3276.5, -3276.5, 327.65, -327.65,32764, -32764, 3276.4, -3276.4, 327.64, -327.64,32763, -32763, 3276.3, -3276.3, 327.63, -327.63,
    32762, -32762, 3276.2, -3276.2, 327.62, -327.62, 32761, -32761, 3276.1, -3276.1, 327.61, -327.61,32760, -32760, 3276.0, -3276.0, 327.60, -327.60,
    32759, -32759, 3275.9, -3275.9, 327.59, -327.59,32751, -32751, 3275.1, -3275.1, 327.51, -327.51,-3277,-3276.9,-38.5,25.4,255,18559,65151
]
def calcular_minuto(fecha_inicio, fecha_fin):
    # Convertir las fechas a objetos datetime
    #fecha_inicio = datetime.strptime(fecha_inicio1, '%Y-%m-%dT%H:%M:%S')
    #fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
    #fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    #fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')   
    # Calcular la diferencia en días
    diferencia = abs((fecha_fin - fecha_inicio).days) 
    if 120 <= diferencia <= 150:
        auto =[60,28]
    elif 90 <= diferencia < 120:
        auto =[55,26]
    elif 60 <= diferencia < 90:
        auto =[50,24]
    elif 45 <= diferencia < 60:
        auto =[45,22]
    elif 30 <= diferencia < 45:
        auto =[40,20]
    elif 24 <= diferencia < 30:
        auto =[35,18]
    elif 18 <= diferencia < 24:
       auto =[30,16]
    elif 12 <= diferencia < 18:
        auto =[25,14]
    elif 9 <= diferencia < 12:
        auto =[20,12]
    elif 6 <= diferencia < 9:
        auto =[15,10]
    elif 3 <= diferencia < 6:
        auto =[10,8]
    elif 1 <= diferencia < 3:
        auto =[5,6]
    else:
        auto =[2,5]
    return auto
    
def depurar_coincidencia(dato, datosDepurar=datosDepurar):
    if dato in datosDepurar:
        return None
    else:
        return dato

def procesar_texto(texto):
    # Dividir el texto en partes separadas por "_"
    partes = texto.split("_") 
    # Convertir cada parte a mayúsculas para capitalizar las palabras
    partes_capitalizadas = [parte.capitalize() for parte in partes]   
    # Unir las partes con espacios en blanco
    texto_procesado = " ".join(partes_capitalizadas) 
    return texto_procesado

def procesar_fecha(fechaI,fechaF="0"):
    if(fechaF=="0"):
        fechaIx=  datetime.fromisoformat(fechaI)-timedelta(hours=12)
        fechaFx = datetime.fromisoformat(fechaI)-timedelta(hours=1)
    else:
        fechaIx=  datetime.fromisoformat(fechaI)
        fechaFx = datetime.fromisoformat(fechaF)-timedelta(hours=1)
    data = [fechaIx,fechaFx]
    return data

def oMeses(dispositivo,fecha_inicio, fecha_fin):
    inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
    fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
    meses = []
    # Iterar sobre los meses en el rango
    while inicio <= fin:
        # Agregar el mes actual a la lista
        meses.append(dispositivo+"_"+str(int(inicio.strftime('%m')))+inicio.strftime('_%Y'))
        # Avanzar al siguiente mes
        inicio += timedelta(days=32)
        inicio = inicio.replace(day=1)
    return meses

async def config(empresa :int):
    notificacions=[]
    database =client["config_ztrack"]
    empresa_config= database.get_collection("empresa_config")
    async for mad in empresa_config.find({"user_id":empresa},{"_id":0}):
        notificacions.append(mad)
    #se debe extraer el primir resultado
    return notificacions[0]

async def data_madurador(notificacion_data: dict) -> dict:
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fech = procesar_fecha(notificacion_data['ultima'])
        bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha(notificacion_data['fechaI'],notificacion_data['fechaF'])
        bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    dataConfig =await config(notificacion_data['empresa'])
    #recorrer array y crear varaibles para insertar
    graph = dataConfig['config_graph']
    listas = {}
    cadena =[]
    listasT={}
    perz = calcular_minuto(fech[0],fech[1])
    #print(bconsultas)
    print(perz)
    minutosP =perz[0]
    print(minutosP)
    delta =perz[1]
    print(delta)
    for i in range(len(graph)):
        nombre_lista = f"{graph[i]['label']}"
        cadena.append(graph[i]['label'])
        lab = procesar_texto(graph[i]['label'])
        listas[nombre_lista] = {
            "data":[],
            "config":[lab,graph[i]['hidden'],graph[i]['color'],graph[i]['tipo']]
        }
    for i in range(len(bconsultas)):
        if(len(bconsultas)==1):
            diferencial =[{"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]
        else:
            if(i==0):
                diferencial =[{"created_at": {"$gte": fech[0]}}]
            else :
                diferencial = [{"created_at": {"$lte": fech[1]}}] if (i==len(bconsultas)-1) else [{"modelo":"THERMOKING"}]
        pip = [
            {"$match": {"$and":diferencial}},  
            {"$project":dataConfig['config_data']},
            {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},
            {"$limit" : notificacion_data['size']},  
        ]
        concepto_ots = []
        database = client[bconsultas[i]]
        madurador = database.get_collection("madurador")
        actual_time = fech[0] 
        actual_intervalo_final =fech[0] +timedelta(minutes=minutosP)
        dato_return_air=None
        async for concepto_ot in madurador.aggregate(pip):
            if(concepto_ot['created_at']<actual_intervalo_final):
                if(dato_return_air is None or abs((concepto_ot['return_air']-dato_return_air)/dato_return_air))* 100 > delta :
                    concepto_ots.append(concepto_ot)
                    for i in range(len(graph)):
                        dato =graph
                        listas[dato[i]['label']]["data"].append(depurar_coincidencia(concepto_ot[dato[i]['label']]))
                dato_return_air = concepto_ot['return_air']
            else:
                concepto_ots.append(concepto_ot)
                for i in range(len(graph)):
                    dato =graph
                    listas[dato[i]['label']]["data"].append(depurar_coincidencia(concepto_ot[dato[i]['label']]))
                actual_time = concepto_ot['created_at']
                actual_intervalo_final = actual_time + timedelta(minutes=minutosP)
                last_return_air = concepto_ot['return_air']
            listasT = {"graph":listas,"table":concepto_ots,"cadena":cadena}
        print(i)
        print(pip)
        #print(listasT)
    return listasT



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

