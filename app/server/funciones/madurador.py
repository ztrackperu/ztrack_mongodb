import json
import mysql.connector
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from fastapi_pagination.ext.motor import paginate

db_connection = mysql.connector.connect(
    host= "localhost",
    user= "ztrack2023",
    passwd= "lpmp2018",
    database="zgroupztrack"
)

def per_actual():
    now = datetime.now()
    mes = now.month 
    per = now.year
    periodo = str(mes)+"_"+str(per)
    return periodo

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


def proporcional_transform(valor, min_entrada, max_entrada, min_salida, max_salida):
    """
    Convierte un valor de un rango de entrada a un rango de salida proporcionalmente.
    """
    return min_salida + (max_salida - min_salida) * ((valor - min_entrada) / (max_entrada - min_entrada))

def procesar_array_etileno(datos):
    resultado = []
    
    for valor in datos:
        if valor > 300:
            resultado.append(None)  # Reemplaza valores mayores a 300 por None
        elif 125 < valor <= 300:
            # Reemplaza valores entre 125 y 300 por números en el rango de 125 a 150 proporcionalmente
            nuevo_valor = proporcional_transform(valor, 125, 300, 125, 150)
            resultado.append(round(nuevo_valor, 1))
        elif 115 < valor <= 125:
            # Mantiene valores entre 115 y 125 igual
            resultado.append(valor)
        elif 50 < valor <= 115:
            # Reemplaza valores entre 50 y 115 por números en el rango de 105 a 115 proporcionalmente
            nuevo_valor = proporcional_transform(valor, 50, 115, 105, 115)
            resultado.append(round(nuevo_valor, 1))
        else:
            # Mantiene valores menores o iguales a 50 igual
            resultado.append(valor)
    
    return resultado

def temp(dato,op):
    res = dato if op==0 else (int(((dato*9/5)+32)*100)/100)
    return res
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

def devolverfecha(utc,fecha):
    terrible=0
    if(utc!=300):
        terrible =300-utc
    #print(terrible)
    #print(fecha)
    #fechaX = datetime.fromisoformat(fecha)+timedelta(minutes=terrible)
    fechaX = fecha+timedelta(minutes=terrible)
    #fechaX =1
    #print(fechaX)
    return fechaX



def procesar_fecha_fila(utc,fechaI,fechaF="0"):
    terrible = 0 ; 
    #print(fechaI)
    #print(fechaF)
    if(utc!=300):
        #terrible =300-utc
        terrible =utc-300
    #print(terrible)
    #print(utc)
    if(fechaF=="0"):
        fechaIx=  datetime.fromisoformat(fechaI)-timedelta(hours=12)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
        fechaFx1 = datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
    else:
        fechaIx=  datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaF)+timedelta(minutes=terrible)
        fechaFx1 = datetime.fromisoformat(fechaF)+timedelta(minutes=terrible)
    data = [fechaIx,fechaFx,fechaFx1]
    #print(data)
    return data

def procesar_fecha(utc,fechaI,fechaF="0"):
    terrible = 0 ; 
    #print(fechaI)
    #print(fechaF)
    if(utc!=300):
        #terrible =300-utc
        terrible =utc-300
    #print(terrible)
    #print(utc)
    if(fechaF=="0"):
        fechaIx=  datetime.fromisoformat(fechaI)-timedelta(hours=12)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaI)-timedelta(hours=1)+timedelta(minutes=terrible)
        fechaFx1 = datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
    else:
        fechaIx=  datetime.fromisoformat(fechaI)+timedelta(minutes=terrible)
        fechaFx = datetime.fromisoformat(fechaF)-timedelta(hours=1)+timedelta(minutes=terrible)
        fechaFx1 = datetime.fromisoformat(fechaF)+timedelta(minutes=terrible)
    data = [fechaIx,fechaFx,fechaFx1]
    #print(data)
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

def analisis_dato(dato,tipo,c_f):
    #dato=float(dato) if dato else None
    #print(dato)
    #print(tipo)
    if dato != None :
        if(tipo==1):
            full = dato if -45 <= dato < 130 else None
            full = full if c_f==0 else (int(((dato*9/5)+32)*10)/10)
        elif(tipo==2):
            full = dato if 0 <= dato< 100 else None
        elif(tipo==3):
            full = dato if 0 <= dato <= 260 else None
        elif(tipo==0):
            full=dato
        else:
            full = 100 if dato==0 or dato==3 else 0
    else :
        full =None
    #return full
    #print(full)
    return full


async def config(empresa :int):
    notificacions=[]
    database =client["config_ztrack"]
    empresa_config= database.get_collection("empresa_config")
    async for mad in empresa_config.find({"user_id":empresa},{"_id":0}):
        notificacions.append(mad)
    #se debe extraer el primir resultado
    return notificacions[0]


async def data_tunel(notificacion_data: dict) -> dict:
    #capturar hora 
    #desglozar la data y almacenar en base de datos REPOSITORIO_MES_AÑO
    palm = "REPOSITORIO_"+per_actual()
    database = client[palm]
    tunel = database.get_collection("tunel")
    #insertar el dato 
    fet =datetime.now()
    #part = fet.strftime('%d_%m_%Y')
    #colect ="Datos_"+part
    #print(colect)
    notificacion_data['fecha'] = fet
    print(notificacion_data)
    notificacion = await tunel.insert_one(notificacion_data)
    new_notificacion = await tunel.find_one({"_id": notificacion.inserted_id},{"_id":0})
    #return notificacion_helper(new_notificacion)
    print(palm)
    return new_notificacion

async def data_wonderful(notificacion_data: dict) -> dict:
    #capturar hora 
    #desglozar la data y almacenar en base de datos REPOSITORIO_MES_AÑO
    palm = "WONDERFUL_"+per_actual()
    database = client[palm]
    cadenaWonderful = notificacion_data['data']
    listaWonderful = cadenaWonderful.split(",")
    device = listaWonderful[2]
    deviceW = device.split("|")
    deviceW1 =deviceW[0]

    #tunel = database.get_collection("tunel")
    tunel = database.get_collection(deviceW1)
    fet =datetime.now()
    notificacion_data['fecha'] = fet
    print(notificacion_data)
    Trama = notificacion_data['data']
    print(Trama)
    trama_d = Trama.split(",")
    print(trama_d[0])
    notificacion = await tunel.insert_one(notificacion_data)
    new_notificacion = await tunel.find_one({"_id": notificacion.inserted_id},{"_id":0})
    #return notificacion_helper(new_notificacion)
    #print(palm)
    #aqui realizamos la consulta a la base de datos para especiifcar si hay comandos pendientes 
    comandos_pendientes ="No existe comandos pendientes"
    comandos = database.get_collection("comandos")
    if trama_d[0] =="1CR3":
        print(" estamos dentro del analisis")
        print(deviceW1)
        comando_existe = await comandos.find_one({"estado":1,"equipo":deviceW1},{"_id":0})
        if comando_existe :
            comandos_pendientes = comando_existe['comando']
            #actualizar para enviar solo una vez 
            comandos.update_one({"estado":1,"equipo":deviceW1},{"$set": {"estado":0,"fecha_ejecucion":fet}})
    return comandos_pendientes


async def data_madurador(notificacion_data: dict) -> dict:
    #print(notificacion_data['utc'])
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fech = procesar_fecha(notificacion_data['utc'],notificacion_data['ultima'])
        bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha(notificacion_data['utc'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    dataConfig =await config(notificacion_data['empresa'])
    graph = dataConfig['config_graph']
    listas = {}
    cadena =[]
    m_d = calcular_minuto(fech[0],fech[1])
    for i in range(len(graph)):
        nombre_lista = f"{graph[i]['label']}"
        cadena.append(graph[i]['label'])
        lab = procesar_texto(graph[i]['label'])
        listas[nombre_lista] = {"data":[],"config":[lab,graph[i]['hidden'],graph[i]['color'],graph[i]['tipo']]}
    for i in range(len(bconsultas)):
        if(len(bconsultas)==1):
            diferencial =[{"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]
        else:
            if(i==0):
                diferencial =[{"created_at": {"$gte": fech[0]}}]
            else :
                diferencial = [{"created_at": {"$lte": fech[1]}}] if (i==len(bconsultas)-1) else [{"modelo":"THERMOKING"}]
        pip = [{"$match": {"$and":diferencial}},  {"$project":dataConfig['config_data']},
                {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},{"$limit" : notificacion_data['size']}]
        concepto_ots = []
        database = client[bconsultas[i]]
        madurador = database.get_collection("madurador")
        actual_time = fech[0] 
        actual_intervalo_final =fech[0] +timedelta(minutes=m_d[0])
        dato_return_air=None
        async for concepto_ot in madurador.aggregate(pip):
            if(concepto_ot['created_at']<actual_intervalo_final):
                dato_return_air = None if dato_return_air==0  else dato_return_air
                if(dato_return_air is None or abs((concepto_ot['return_air']-dato_return_air)/dato_return_air))* 100 > m_d[1] :
                    #concepto_ots.append(concepto_ot)
                    for i in range(len(graph)):
                        dato =graph
                        if dato[i]['label']=='created_at':
                            listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
                        else:
                            listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
                dato_return_air = concepto_ot['return_air']
            else:
                #concepto_ots.append(concepto_ot)
                for i in range(len(graph)):
                    dato =graph
                    if dato[i]['label']=='created_at':
                        listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
                    else:
                        listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
                actual_time = concepto_ot['created_at']
                actual_intervalo_final = actual_time + timedelta(minutes=m_d[0])
                last_return_air = concepto_ot['return_air']
    database = client[bconsultas[len(bconsultas)-1]]
    madurador = database.get_collection("madurador")
    pip = [{"$match": {"$and":[{"created_at": {"$gte": fech[1]}},{"created_at": {"$lte": fech[2]}}]}},  {"$project":dataConfig['config_data']},
    {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},{"$limit" : notificacion_data['size']}]
    async for concepto_ot in madurador.aggregate(pip):
        for i in range(len(graph)):
            dato =graph
            if dato[i]['label']=='created_at':
                listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
            else:
                listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
    #print(fech[0])
    #print(fech[2])
    listasT = {"graph":listas,"table":concepto_ots,"cadena":cadena,"temperature":dataConfig['c_f'],"date":[devolverfecha(notificacion_data['utc'],fech[0]),devolverfecha(notificacion_data['utc'],fech[2])]}
    return listasT



async def data_madurador_filadelfia(notificacion_data: dict) -> dict:
    #print(notificacion_data['utc'])
    if(notificacion_data['fechaF']=="0" and notificacion_data['fechaI']=="0"):
        fech = procesar_fecha_fila(notificacion_data['utc'],notificacion_data['ultima'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['ultima'],notificacion_data['ultima'])
    else : 
        fech = procesar_fecha_fila(notificacion_data['utc'],notificacion_data['fechaI'],notificacion_data['fechaF'])
        #bconsultas =oMeses(notificacion_data['device'],notificacion_data['fechaI'],notificacion_data['fechaF'])
    dataConfig =await config(notificacion_data['empresa'])
    graph = dataConfig['config_graph']
    listas = {}
    cadena =[]
    m_d = calcular_minuto(fech[0],fech[1])
    for i in range(len(graph)):
        nombre_lista = f"{graph[i]['label']}"
        cadena.append(graph[i]['label'])
        lab = procesar_texto(graph[i]['label'])
        listas[nombre_lista] = {"data":[],"config":[lab,graph[i]['hidden'],graph[i]['color'],graph[i]['tipo']]}

    bconsultas="ztrack_ja"
    diferencial =[{"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}},{"telemetria_id":notificacion_data['device']}]
    pip = [{"$match": {"$and":diferencial}},  {"$project":dataConfig['config_data']},
                {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},{"$limit" : notificacion_data['size']}]
    concepto_ots = []
    database = client[bconsultas]
    madurador = database.get_collection("madurador")
    actual_time = fech[0] 
    actual_intervalo_final =fech[0] +timedelta(minutes=m_d[0])
    dato_return_air=None

    async for concepto_ot in madurador.aggregate(pip):
        for i in range(len(graph)):
            dato =graph
            if dato[i]['label']=='created_at':
                listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
            else:
                listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
    analizar =listas['ethylene']['data']
    transformada =procesar_array_etileno(analizar)
    listas['ethylene']['data']=transformada
    listasT = {"graph":listas,"table":"concepto_ots","cadena":cadena,"temperature":dataConfig['c_f'],"date":[devolverfecha(notificacion_data['utc'],fech[0]),devolverfecha(notificacion_data['utc'],fech[2])]}
    return listasT
    async for concepto_ot in madurador.aggregate(pip):
        if(concepto_ot['created_at']<actual_intervalo_final):
            dato_return_air = None if dato_return_air==0  else dato_return_air
            if(dato_return_air is None or abs((concepto_ot['return_air']-dato_return_air)/dato_return_air))* 100 > m_d[1] :
                #concepto_ots.append(concepto_ot)
                for i in range(len(graph)):
                    dato =graph
                    if dato[i]['label']=='created_at':
                        listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
                    else:
                        listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
            dato_return_air = concepto_ot['return_air']
        else:
            #concepto_ots.append(concepto_ot)
            for i in range(len(graph)):
                dato =graph
                if dato[i]['label']=='created_at':
                    listas[dato[i]['label']]["data"].append(devolverfecha(notificacion_data['utc'],concepto_ot[dato[i]['label']]))
                else:
                    listas[dato[i]['label']]["data"].append(analisis_dato(depurar_coincidencia(concepto_ot[dato[i]['label']]), listas[dato[i]['label']]["config"][3],dataConfig['c_f']))
            actual_time = concepto_ot['created_at']
            actual_intervalo_final = actual_time + timedelta(minutes=m_d[0])
            last_return_air = concepto_ot['return_air']
    

    listasT = {"graph":listas,"table":"concepto_ots","cadena":cadena,"temperature":dataConfig['c_f'],"date":[devolverfecha(notificacion_data['utc'],fech[0]),devolverfecha(notificacion_data['utc'],fech[2])]}
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

async def homologar_tunel_2() -> dict:
    #establecer conexion con datos en mongodb 
    #normalizar los datos y actualizar infromacion en tiempo real en mysql
    #insertar trama en base de mongodb para su uso en la plataforma 

    #consultar datos de mysql de tunel ZGTU0015
    dat =''

    #extramemos la informacion en bruto del equipo
    #databaseMongo = client["REPOSITORIO_6_2024"]
    databaseMongo = client["REPOSITORIO_7_2024"]
    
    collectionMongo = databaseMongo.get_collection("tunel")

    #database =client["config_ztrack"]
    #empresa_config= database.get_collection("empresa_config")
    #async for mad in empresa_config.find({"user_id":empresa},{"_id":0}):
        #notificacions.append(mad)
    #se debe extraer el primir resultado
    #return notificacions[0]
    
    #querymongo = collectionMongo.find({"status":1}).sort("fecha",1)
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):

        #db1 = client.ZGTU0015_6_2024
        #collection1 = db1.madurador
        #query1 = collection1.find().sort("id",-1).limit(1)
        #databaseMongo2 = client["ZGTU0015_6_2024"]
        #databaseMongo2 = client["ZGTU0015_7_2024"]
        #para la base de datos principal
        databaseMongo2 = client["ztrack_ja"]

        collectionMongo2 = databaseMongo2.get_collection("madurador")

        query1 = collectionMongo2.find_one()
        print(query1)
        id =1000000000
        if query1:
            #query2 = collectionMongo2.find().sort("id",-1).limit(1)
            async for y in collectionMongo2.find({ "telemetria_id": 1000000 }).sort("id",-1).limit(1):
                print(y)
                id =y["id"] +1
        
        print(id)
        print(x['fecha'])
        datito = x['data']
        paquete = datito.split(',') 
        print(datito)
        print(float(paquete[42]))
        #contruir objeto 
        objeto1 = {
            "id": id,
            "set_point": float(paquete[3]), 
            "temp_supply_1": float(paquete[4]),
            "temp_supply_2": float(paquete[5]),
            "return_air": float(paquete[6]), 
            "evaporation_coil": float(paquete[7]),
            "condensation_coil": float(paquete[8]),
            "compress_coil_1": float(paquete[9]),
            "compress_coil_2": float(paquete[10]), 
            "ambient_air": float(paquete[11]), 
            "cargo_1_temp": float(paquete[12]),
            "cargo_2_temp": float(paquete[13]), 
            "cargo_3_temp": float(paquete[14]), 
            "cargo_4_temp": float(paquete[15]), 
            "relative_humidity": float(paquete[16]), 
            "avl": float(paquete[17]), 
            "suction_pressure": float(paquete[18]), 
            "discharge_pressure": float(paquete[19]), 
            "line_voltage": float(paquete[20]), 
            "line_frequency": float(paquete[21]), 
            "consumption_ph_1": float(paquete[22]), 
            "consumption_ph_2": float(paquete[23]), 
            "consumption_ph_3": float(paquete[24]), 
            "co2_reading": float(paquete[25]), 
            "o2_reading": float(paquete[26]), 
            "evaporator_speed": float(paquete[27]), 
            "condenser_speed": float(paquete[28]),
            "battery_voltage": float(paquete[29]),
            "power_kwh": float(paquete[30]),
            "power_trip_reading": float(paquete[31]),
            "power_trip_duration": None,
            "suction_temp": None,
            "discharge_temp": None,
            "supply_air_temp": None,
            "return_air_temp": None,
            "dl_battery_temp": None,
            "dl_battery_charge": None,
            "power_consumption": None,
            "power_consumption_avg": None,
            "alarm_present": None, 
            "capacity_load": None,
            "power_state": float(paquete[42]),
            "controlling_mode": "1",
            "humidity_control": None,
            "humidity_set_point": None,
            "fresh_air_ex_mode": None,
            "fresh_air_ex_rate": None,
            "fresh_air_ex_delay": None,
            "set_point_o2": None,
            "set_point_co2": None,
            "defrost_term_temp": None,
            "defrost_interval": None,
            "water_cooled_conde": None,
            "usda_trip": None,
            "evaporator_exp_valve": None,
            "suction_mod_valve": None,
            "hot_gas_valve": None,
            "economizer_valve": None,
            "ethylene": None,
            "stateProcess": None,
            "stateInyection": None,
            "timerOfProcess": None,
            "modelo": "THERMOKING",
            "latitud": -11.9803,
            "longitud": -77.1226,
            "created_at": x['fecha'],
            "telemetria_id": 1000000,
            "inyeccion_etileno": None,
            "defrost_prueba": None,
            "ripener_prueba": None,
            "sp_ethyleno": None,
            "inyeccion_hora": None,
            "inyeccion_pwm": None,
            "extra_1": 0,
            "extra_2": 0,
            "extra_3": 0,
            "extra_4": 0,
            "extra_5": 0
        }
        #print(objeto1)
        #guardar en base de datos 
        collectionMongo2.insert_one(objeto1)

        db_cursor = db_connection.cursor()
        #ZGRU9015808
        #buscar data en mysql del tunel
        db_cursor.execute("SELECT * FROM  contenedores WHERE nombre_contenedor='ZGTU0015'")
          
        for db in db_cursor :
            if db!="" :
                print(db)
                update_tunel= (
                    "UPDATE contenedores SET set_point = %s,temp_supply_1 = %s,return_air = %s,evaporation_coil = %s,condensation_coil = %s"
                    ",compress_coil_1 = %s,ambient_air = %s,cargo_1_temp = %s,cargo_2_temp = %s,cargo_3_temp = %s,cargo_4_temp = %s,relative_humidity = %s"
                    ",avl = %s,suction_pressure = %s,discharge_pressure = %s,line_voltage = %s,line_frequency = %s,consumption_ph_1 = %s,consumption_ph_2 = %s"
                    ",consumption_ph_3 = %s,co2_reading = %s,o2_reading = %s,evaporator_speed = %s,condenser_speed = %s,battery_voltage = %s,power_kwh = %s"
                    ",power_trip_reading = %s,power_state = %s,ultima_fecha = %s"
                    "WHERE nombre_contenedor='ZGTU0015'")
                    #telemetria_id=1000000 
                data_tunel =(float(paquete[3]),float(paquete[4]),float(paquete[6]),float(paquete[7]),float(paquete[8]),float(paquete[9]),float(paquete[11])
                             ,float(paquete[12]),float(paquete[13]),float(paquete[14]),float(paquete[15]),float(paquete[16]),float(paquete[17]),float(paquete[18])
                             ,float(paquete[19]),float(paquete[20]),float(paquete[21]),float(paquete[22]),float(paquete[23]),float(paquete[24]),float(paquete[25])
                             ,float(paquete[26]),float(paquete[27]),float(paquete[28]),float(paquete[29]),float(paquete[30]),float(paquete[31]),float(paquete[42])
                              ,x['fecha']                                                                                                                       
                             )
                # Insert new employee
            db_cursor1 = db_connection.cursor()
            db_cursor1.execute(update_tunel, data_tunel)
            #emp_no = cursor.lastrowid
                
            #actualizar datos del tunel 
            db_connection.commit()
            db_cursor1.close()
        
        db_cursor.close()
        dat = db
    db_connection.close()
      
    #dat ="olitas"
    return dat

def obtener_mes_y_anio_actual():
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()
    
    # Obtener el mes y el año
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year
    
    # Formatear la cadena mes_año
    mes_anio_str = f"{mes_actual}_{anio_actual}"
    return mes_anio_str

# Ejemplo de uso
#print(obtener_mes_y_anio_actual())

def convertir_a_float(dato):
    if isinstance(dato, float):
        return dato
    try:
        float_value = float(dato)
        return float_value
    except ValueError:
        return None
    

async def homologar_wonderful_zgru1090804_2() -> dict:
    #ZGRU1090804 -> 33
    #ZGRU2009227 -> 259
    #ZGRU2008220 -> 260
    #ZGRU2232647 -> 258
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    tele_wonderful =33
    nombre_dispositivo='ZGRU1090804'
    controlTelemetria = await collectionControl.find_one({"telemetria_id":tele_wonderful})
    #print(controlTelemetria)
    idProgre = 10000000000
    factorBusqueda ={}
    estadoC=0
    print(controlTelemetria)
    if controlTelemetria :
        #print("tenemos datos")
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        print(fechaId)
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        print(factorBusqueda)
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection("ZGRU1090804")
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curA = cnx.cursor(buffered=True)
    curB = cnx.cursor(buffered=True)
    dataContenedor = curA.execute("SELECT * FROM contenedores WHERE nombre_contenedor='ZGRU1090804'")
    rows = curA.fetchall()
    conMysql =[]
    for row in rows :
        conMysql.append(row)
        print(row)

    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        print(x)
        fecha_wonderful=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                #aqui debe de guardarse en la tabal control para que quede constancia de la ultima trama 
                if  len(vali)==70:
                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[3]), 
                            "temp_supply_1": convertir_a_float(vali[4]),
                            "temp_supply_2": convertir_a_float(vali[5]),
                            "return_air": convertir_a_float(vali[6]), 
                            "evaporation_coil": convertir_a_float(vali[7]),
                            "condensation_coil": convertir_a_float(vali[8]),
                            "compress_coil_1": convertir_a_float(vali[9]),
                            "compress_coil_2": convertir_a_float(vali[10]), 
                            "ambient_air": convertir_a_float(vali[11]), 
                            "cargo_1_temp": convertir_a_float(vali[12]),
                            "cargo_2_temp": convertir_a_float(vali[13]), 
                            "cargo_3_temp": convertir_a_float(vali[14]), 
                            "cargo_4_temp": convertir_a_float(vali[15]), 
                            "relative_humidity": convertir_a_float(vali[16]), 
                            "avl": convertir_a_float(vali[17]), 
                            "suction_pressure": convertir_a_float(vali[18]), 
                            "discharge_pressure": convertir_a_float(vali[19]), 
                            "line_voltage": convertir_a_float(vali[20]), 
                            "line_frequency": convertir_a_float(vali[21]), 
                            "consumption_ph_1": convertir_a_float(vali[22]), 
                            "consumption_ph_2": convertir_a_float(vali[23]), 
                            "consumption_ph_3": convertir_a_float(vali[24]), 
                            "co2_reading": convertir_a_float(vali[25]), 
                            "o2_reading": convertir_a_float(vali[26]), 
                            "evaporator_speed": convertir_a_float(vali[27]), 
                            "condenser_speed": convertir_a_float(vali[28]),
                            "power_kwh": convertir_a_float(vali[29]),
                            "power_trip_reading": convertir_a_float(vali[30]),
                            "suction_temp": convertir_a_float(vali[31]),
                            "discharge_temp": convertir_a_float(vali[32]),
                            "supply_air_temp": convertir_a_float(vali[33]),
                            "return_air_temp": convertir_a_float(vali[34]),
                            "dl_battery_temp": convertir_a_float(vali[35]),
                            "dl_battery_charge": convertir_a_float(vali[36]),
                            "power_consumption": convertir_a_float(vali[37]),
                            "power_consumption_avg": convertir_a_float(vali[38]),
                            "alarm_present": convertir_a_float(vali[39]),
                            "capacity_load": convertir_a_float(vali[40]),
                            "power_state": convertir_a_float(vali[41]), 
                            "controlling_mode": vali[42],
                            "humidity_control": convertir_a_float(vali[43]),
                            "humidity_set_point": convertir_a_float(vali[44]),
                            "fresh_air_ex_mode": convertir_a_float(vali[45]),
                            "fresh_air_ex_rate": convertir_a_float(vali[46]),
                            "fresh_air_ex_delay": convertir_a_float(vali[47]),
                            "set_point_o2": convertir_a_float(vali[48]),
                            "set_point_co2": convertir_a_float(vali[49]),
                            "defrost_term_temp": convertir_a_float(vali[50]),
                            "defrost_interval": convertir_a_float(vali[51]),
                            "water_cooled_conde": convertir_a_float(vali[52]),
                            "usda_trip": convertir_a_float(vali[53]),
                            "evaporator_exp_valve": convertir_a_float(vali[54]),
                            "suction_mod_valve": convertir_a_float(vali[55]),
                            "hot_gas_valve": convertir_a_float(vali[56]),
                            "economizer_valve": convertir_a_float(vali[57]),
                            "ethylene": convertir_a_float(vali[58]),
                            "stateProcess": vali[59],
                            "stateInyection": vali[60],
                            "timerOfProcess": convertir_a_float(vali[61]),
                            "battery_voltage": convertir_a_float(vali[62]),
                            "power_trip_duration":convertir_a_float(vali[63]),
                            "modelo": vali[64],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": fecha_wonderful,
                            "telemetria_id": tele_wonderful,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[67]),
                            "inyeccion_hora": convertir_a_float(vali[68]),
                            "inyeccion_pwm": convertir_a_float(vali[69]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0
                        }
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    collectionMongoH.insert_one(objetoV)

                    base_novo = nombre_dispositivo+"_"+datazo
                    databaseMongo_NOVO = client[base_novo]
                    collectionMongo_NOVO = databaseMongo_NOVO.get_collection("madurador")
                    collectionMongo_NOVO.insert_one(objetoV)



                    objetoControl ={
                        "id":idProgre,
                        "telemetria_id":tele_wonderful,
                        "fecha":fecha_wonderful
                    }
                    if estadoC==1 :
                        #actualizar
                        collectionControl.update_one({"telemetria_id":tele_wonderful,},{"$set": {"id":idProgre,"fecha":fecha_wonderful}})
                    else :
                        #grabar
                        collectionControl.insert_one(objetoControl)
                        estadoC=1
                    curB = cnx.cursor()
                    update_old_salary = (
                    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                     " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                    curB.execute(update_old_salary, (fecha_wonderful, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                     objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                     objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                     objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                     objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                     objetoV['telemetria_id'],  ))
                    cnx.commit()
    cnx.close()
    return idProgre





async def homologar_wonderful_zgru1090804() -> dict:
    #preguntar fecha mes_año 07_2024
    datazo = obtener_mes_y_anio_actual()
    #print(datazo)
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]  
    collectionMongo = databaseMongo.get_collection("ZGRU1090804")
    trama=''
        # inicio de id para las telemetrias como referencias 
        #ZGRU1090804 -> 10000000000
        #ZGRU2009227 -> 11000000000
        #ZGRU2008220 -> 12000000000
        #ZGRU2232647 -> 13000000000
    idProgre = 10000000000
    #async for x in collectionMongo.find({"status":1}).sort("fecha",1).limit(10):
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):

        cad =x['data']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                if len(vali)==70:
                    print("listo pa insertar")
                    #aqui realizar la insercion de datos 
                    fecha_wonderful=x['fecha']
                    #telemetria_id de los dispositivos
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    tele_wonderful=33                    

                    objetoV = {
                        "id": idProgre,
                        "set_point": float(vali[3]), 
                        "temp_supply_1": float(vali[4]),
                        "temp_supply_2": float(vali[5]),
                        "return_air": float(vali[6]), 
                        "evaporation_coil": float(vali[7]),
                        "condensation_coil": float(vali[8]),
                        "compress_coil_1": float(vali[9]),
                        "compress_coil_2": float(vali[10]), 
                        "ambient_air": float(vali[11]), 
                        "cargo_1_temp": float(vali[12]),
                        "cargo_2_temp": float(vali[13]), 
                        "cargo_3_temp": float(vali[14]), 
                        "cargo_4_temp": float(vali[15]), 
                        "relative_humidity": float(vali[16]), 
                        "avl": float(vali[17]), 
                        "suction_pressure": float(vali[18]), 
                        "discharge_pressure": float(vali[19]), 
                        "line_voltage": float(vali[20]), 
                        "line_frequency": float(vali[21]), 
                        "consumption_ph_1": float(vali[22]), 
                        "consumption_ph_2": float(vali[23]), 
                        "consumption_ph_3": float(vali[24]), 
                        "co2_reading": float(vali[25]), 
                        "o2_reading": float(vali[26]), 
                        "evaporator_speed": float(vali[27]), 
                        "condenser_speed": float(vali[28]),
                        "power_kwh": float(vali[29]),
                        "power_trip_reading": float(vali[30]),
                        "suction_temp": float(vali[31]),
                        "discharge_temp": float(vali[32]),
                        "supply_air_temp": float(vali[33]),
                        "return_air_temp": float(vali[34]),
                        "dl_battery_temp": float(vali[35]),
                        "dl_battery_charge": float(vali[36]),
                        "power_consumption": float(vali[37]),
                        "power_consumption_avg": float(vali[38]),
                        "alarm_present": float(vali[39]),
                        "capacity_load": float(vali[40]),
                        "power_state": float(vali[41]), 
                        "controlling_mode": vali[42],
                        "humidity_control": float(vali[43]),
                        "humidity_set_point": float(vali[44]),
                        "fresh_air_ex_mode": float(vali[45]),
                        "fresh_air_ex_rate": float(vali[46]),
                        "fresh_air_ex_delay": float(vali[47]),
                        "set_point_o2": float(vali[48]),
                        "set_point_co2": float(vali[49]),
                        "defrost_term_temp": float(vali[50]),
                        "defrost_interval": float(vali[51]),
                        "water_cooled_conde": float(vali[52]),
                        "usda_trip": float(vali[53]),
                        "evaporator_exp_valve": float(vali[54]),
                        "suction_mod_valve": float(vali[55]),
                        "hot_gas_valve": float(vali[56]),
                        "economizer_valve": float(vali[57]),
                        "ethylene": float(vali[58]),
                        "stateProcess": vali[59],
                        "stateInyection": vali[60],
                        "timerOfProcess": float(vali[61]),
                        "battery_voltage": float(vali[62]),
                        "power_trip_duration":float(vali[63]),
                        "modelo": vali[64],
                        "latitud": 35.7396,
                        "longitud":  -119.238,
                        "created_at": fecha_wonderful,
                        "telemetria_id": tele_wonderful,
                        "inyeccion_etileno": 0,
                        "defrost_prueba": 0,
                        "ripener_prueba": 0,
                        "sp_ethyleno": int(vali[67]),
                        "inyeccion_hora": int(vali[68]),
                        "inyeccion_pwm": float(vali[69]),
                        "extra_1": 0,
                        "extra_2": 0,
                        "extra_3": 0,
                        "extra_4": 0,
                        "extra_5": 0
                    }

                    #actualizar en base de mysql
                    #insertaren bd mongodb 
                    #crear dat h_ZGRU1090804
                    #databaseMongoH = client['Homologar']  
                    #collectionMongoH = databaseMongoH.get_collection("ZGRU1090804")
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    #actualizar el estado de la trama 
                    collectionMongo.update
                    collectionMongoH.insert_one(objetoV)

        #print(f2[2])
    return baseD




async def homologar_wonderful_zgru2009227_2() -> dict:
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    tele_wonderful =259
    nombre_dispositivo='ZGRU2009227'
    controlTelemetria = await collectionControl.find_one({"telemetria_id":tele_wonderful})
    #print(controlTelemetria)
    idProgre = 11000000000
    factorBusqueda ={}
    estadoC=0
    print(controlTelemetria)
    if controlTelemetria :
        #print("tenemos datos")
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        print(fechaId)
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        print(factorBusqueda)
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection("ZGRU2009227")

    #cnx = db_connection
    # Get two buffered cursors

    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curA = cnx.cursor(buffered=True)
    curB = cnx.cursor(buffered=True)

    # Query to get employees who joined in a period defined by two dates
    query = ("SELECT * FROM contenedores "
                "WHERE nombre_contenedor= %s LIMIT 1")
    
    #dataContenedor = curA.execute(query, (nombre_dispositivo,))
    dataContenedor = curA.execute("SELECT * FROM contenedores WHERE nombre_contenedor='ZGRU2009227'")
    rows = curA.fetchall()
    conMysql =[]
    for row in rows :
        conMysql.append(row)
        print(row)
    #curA.close()

    #for (nombre_contenedor, ultima_fecha, power_state) in dataContenedor:
        #print("datito")
        #print(nombre_contenedor)
        #print(power_state)
        #print(ultima_fecha)
        #print("datito")
    #print(dataContenedor)


    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        print(x)
        fecha_wonderful=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                #aqui debe de guardarse en la tabal control para que quede constancia de la ultima trama 
                if  len(vali)==70:
                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[3]), 
                            "temp_supply_1": convertir_a_float(vali[4]),
                            "temp_supply_2": convertir_a_float(vali[5]),
                            "return_air": convertir_a_float(vali[6]), 
                            "evaporation_coil": convertir_a_float(vali[7]),
                            "condensation_coil": convertir_a_float(vali[8]),
                            "compress_coil_1": convertir_a_float(vali[9]),
                            "compress_coil_2": convertir_a_float(vali[10]), 
                            "ambient_air": convertir_a_float(vali[11]), 
                            "cargo_1_temp": convertir_a_float(vali[12]),
                            "cargo_2_temp": convertir_a_float(vali[13]), 
                            "cargo_3_temp": convertir_a_float(vali[14]), 
                            "cargo_4_temp": convertir_a_float(vali[15]), 
                            "relative_humidity": convertir_a_float(vali[16]), 
                            "avl": convertir_a_float(vali[17]), 
                            "suction_pressure": convertir_a_float(vali[18]), 
                            "discharge_pressure": convertir_a_float(vali[19]), 
                            "line_voltage": convertir_a_float(vali[20]), 
                            "line_frequency": convertir_a_float(vali[21]), 
                            "consumption_ph_1": convertir_a_float(vali[22]), 
                            "consumption_ph_2": convertir_a_float(vali[23]), 
                            "consumption_ph_3": convertir_a_float(vali[24]), 
                            "co2_reading": convertir_a_float(vali[25]), 
                            "o2_reading": convertir_a_float(vali[26]), 
                            "evaporator_speed": convertir_a_float(vali[27]), 
                            "condenser_speed": convertir_a_float(vali[28]),
                            "power_kwh": convertir_a_float(vali[29]),
                            "power_trip_reading": convertir_a_float(vali[30]),
                            "suction_temp": convertir_a_float(vali[31]),
                            "discharge_temp": convertir_a_float(vali[32]),
                            "supply_air_temp": convertir_a_float(vali[33]),
                            "return_air_temp": convertir_a_float(vali[34]),
                            "dl_battery_temp": convertir_a_float(vali[35]),
                            "dl_battery_charge": convertir_a_float(vali[36]),
                            "power_consumption": convertir_a_float(vali[37]),
                            "power_consumption_avg": convertir_a_float(vali[38]),
                            "alarm_present": convertir_a_float(vali[39]),
                            "capacity_load": convertir_a_float(vali[40]),
                            "power_state": convertir_a_float(vali[41]), 
                            "controlling_mode": vali[42],
                            "humidity_control": convertir_a_float(vali[43]),
                            "humidity_set_point": convertir_a_float(vali[44]),
                            "fresh_air_ex_mode": convertir_a_float(vali[45]),
                            "fresh_air_ex_rate": convertir_a_float(vali[46]),
                            "fresh_air_ex_delay": convertir_a_float(vali[47]),
                            "set_point_o2": convertir_a_float(vali[48]),
                            "set_point_co2": convertir_a_float(vali[49]),
                            "defrost_term_temp": convertir_a_float(vali[50]),
                            "defrost_interval": convertir_a_float(vali[51]),
                            "water_cooled_conde": convertir_a_float(vali[52]),
                            "usda_trip": convertir_a_float(vali[53]),
                            "evaporator_exp_valve": convertir_a_float(vali[54]),
                            "suction_mod_valve": convertir_a_float(vali[55]),
                            "hot_gas_valve": convertir_a_float(vali[56]),
                            "economizer_valve": convertir_a_float(vali[57]),
                            "ethylene": convertir_a_float(vali[58]),
                            "stateProcess": vali[59],
                            "stateInyection": vali[60],
                            "timerOfProcess": convertir_a_float(vali[61]),
                            "battery_voltage": convertir_a_float(vali[62]),
                            "power_trip_duration":convertir_a_float(vali[63]),
                            "modelo": vali[64],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": fecha_wonderful,
                            "telemetria_id": tele_wonderful,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[67]),
                            "inyeccion_hora": convertir_a_float(vali[68]),
                            "inyeccion_pwm": convertir_a_float(vali[69]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0
                        }
                    
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    collectionMongoH.insert_one(objetoV)

                    base_novo = nombre_dispositivo+"_"+datazo
                    databaseMongo_NOVO = client[base_novo]
                    collectionMongo_NOVO = databaseMongo_NOVO.get_collection("madurador")
                    collectionMongo_NOVO.insert_one(objetoV)

                    objetoControl ={
                        "id":idProgre,
                        "telemetria_id":tele_wonderful,
                        "fecha":fecha_wonderful
                    }
                    if estadoC==1 :
                        #actualizar
                        collectionControl.update_one({"telemetria_id":tele_wonderful,},{"$set": {"id":idProgre,"fecha":fecha_wonderful}})
                    else :
                        #grabar
                        collectionControl.insert_one(objetoControl)
                        estadoC=1

                    # Connect with the MySQL Server
                    #cnx = mysql.connector.connect(user='scott', database='employees')


                    # UPDATE and INSERT statements for the old and new salary
                    #update_old_contenedor = (
                    #"UPDATE contenedores SET ultima_fecha = %s ,set_point =  %s,temp_supply_1= %s , return_air= % , ambient_air= %s ,relative_humidity= %s"
                    #",power_state = %s WHERE nombre_contenedor= %s")
                    #insert_new_salary = (
                    #"INSERT INTO salaries (emp_no, from_date, to_date, salary) "
                    #"VALUES (%s, %s, %s, %s)")

                    # Select the employees getting a raise

                    
                    curB = cnx.cursor()
                    update_old_salary = (
                    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                     " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                    curB.execute(update_old_salary, (fecha_wonderful, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                     objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                     objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                     objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                     objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                     objetoV['telemetria_id'],  ))
                    cnx.commit()
    cnx.close()

    return idProgre


async def homologar_wonderful_zgru2009227() -> dict:
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]  
    collectionMongo = databaseMongo.get_collection("ZGRU2009227")
    #analizar el resultado de la coleccion de control 
    collectionControl =databaseMongo.get_collection("control")
    trama=''
        # inicio de id para las telemetrias como referencias 
        #ZGRU1090804 -> 10000000000
        #ZGRU2009227 -> 11000000000
        #ZGRU2008220 -> 12000000000
        #ZGRU2232647 -> 13000000000
    idProgre = 11000000000
    #async for x in collectionMongo.find({"status":1}).sort("fecha",1).limit(10):
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):
        id_actualizar=x['_id']
        print(id_actualizar)
        #{"$set": {"key": "value"}}
        #collectionMongo.update_one({"_id":id_actualizar},{"$set": {"status":0}})
        #controlTelemetria = collectionControl.find_one({"telemetria_id":259})


        cad =x['data']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                if len(vali)==70:
                    print("listo pa insertar")
                    #aqui realizar la insercion de datos 
                    fecha_wonderful=x['fecha']
                    
                    #telemetria_id de los dispositivos
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    tele_wonderful=259                    

                    objetoV = {
                        "id": idProgre,
                        "set_point": float(vali[3]), 
                        "temp_supply_1": float(vali[4]),
                        "temp_supply_2": float(vali[5]),
                        "return_air": float(vali[6]), 
                        "evaporation_coil": float(vali[7]),
                        "condensation_coil": float(vali[8]),
                        "compress_coil_1": float(vali[9]),
                        "compress_coil_2": float(vali[10]), 
                        "ambient_air": float(vali[11]), 
                        "cargo_1_temp": float(vali[12]),
                        "cargo_2_temp": float(vali[13]), 
                        "cargo_3_temp": float(vali[14]), 
                        "cargo_4_temp": float(vali[15]), 
                        "relative_humidity": float(vali[16]), 
                        "avl": float(vali[17]), 
                        "suction_pressure": float(vali[18]), 
                        "discharge_pressure": float(vali[19]), 
                        "line_voltage": float(vali[20]), 
                        "line_frequency": float(vali[21]), 
                        "consumption_ph_1": float(vali[22]), 
                        "consumption_ph_2": float(vali[23]), 
                        "consumption_ph_3": float(vali[24]), 
                        "co2_reading": float(vali[25]), 
                        "o2_reading": float(vali[26]), 
                        "evaporator_speed": float(vali[27]), 
                        "condenser_speed": float(vali[28]),
                        "power_kwh": float(vali[29]),
                        "power_trip_reading": float(vali[30]),
                        "suction_temp": float(vali[31]),
                        "discharge_temp": float(vali[32]),
                        "supply_air_temp": float(vali[33]),
                        "return_air_temp": float(vali[34]),
                        "dl_battery_temp": float(vali[35]),
                        "dl_battery_charge": float(vali[36]),
                        "power_consumption": float(vali[37]),
                        "power_consumption_avg": float(vali[38]),
                        "alarm_present": float(vali[39]),
                        "capacity_load": float(vali[40]),
                        "power_state": float(vali[41]), 
                        "controlling_mode": vali[42],
                        "humidity_control": float(vali[43]),
                        "humidity_set_point": float(vali[44]),
                        "fresh_air_ex_mode": float(vali[45]),
                        "fresh_air_ex_rate": float(vali[46]),
                        "fresh_air_ex_delay": float(vali[47]),
                        "set_point_o2": float(vali[48]),
                        "set_point_co2": float(vali[49]),
                        "defrost_term_temp": float(vali[50]),
                        "defrost_interval": float(vali[51]),
                        "water_cooled_conde": float(vali[52]),
                        "usda_trip": float(vali[53]),
                        "evaporator_exp_valve": float(vali[54]),
                        "suction_mod_valve": float(vali[55]),
                        "hot_gas_valve": float(vali[56]),
                        "economizer_valve": float(vali[57]),
                        "ethylene": float(vali[58]),
                        "stateProcess": vali[59],
                        "stateInyection": vali[60],
                        "timerOfProcess": float(vali[61]),
                        "battery_voltage": float(vali[62]),
                        "power_trip_duration":float(vali[63]),
                        "modelo": vali[64],
                        "latitud": 35.7396,
                        "longitud":  -119.238,
                        "created_at": fecha_wonderful,
                        "telemetria_id": tele_wonderful,
                        "inyeccion_etileno": 0,
                        "defrost_prueba": 0,
                        "ripener_prueba": 0,
                        "sp_ethyleno": int(vali[67]),
                        "inyeccion_hora": int(vali[68]),
                        "inyeccion_pwm": float(vali[69]),
                        "extra_1": 0,
                        "extra_2": 0,
                        "extra_3": 0,
                        "extra_4": 0,
                        "extra_5": 0
                    }


                    #actualizar en base de mysql
                    #insertaren bd mongodb 
                    #crear dat h_ZGRU1090804
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    #databaseMongoH = client['Homologar']  
                    #collectionMongoH = databaseMongoH.get_collection("ZGRU2009227")
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    #result = await coll.update_one({"i": 51}, {"$set": {"key": "value"}})
                    #collectionMongoH.update_one({"_id":id_actualizar},{"status":0})
                    collectionMongoH.insert_one(objetoV)

    return baseD



async def homologar_wonderful_zgru2008220_2() -> dict:
    #ZGRU1090804 -> 33
    #ZGRU2009227 -> 259
    #ZGRU2008220 -> 260
    #ZGRU2232647 -> 258
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    tele_wonderful =260
    nombre_dispositivo='ZGRU2008220'
    controlTelemetria = await collectionControl.find_one({"telemetria_id":tele_wonderful})
    #print(controlTelemetria)
    idProgre = 12000000000
    factorBusqueda ={}
    estadoC=0
    print(controlTelemetria)
    if controlTelemetria :
        #print("tenemos datos")
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        print(fechaId)
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        print(factorBusqueda)
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection("ZGRU2008220")
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curA = cnx.cursor(buffered=True)
    curB = cnx.cursor(buffered=True)
    dataContenedor = curA.execute("SELECT * FROM contenedores WHERE nombre_contenedor='ZGRU2008220'")
    rows = curA.fetchall()
    conMysql =[]
    for row in rows :
        conMysql.append(row)
        print(row)

    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        print(x)
        fecha_wonderful=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                #aqui debe de guardarse en la tabal control para que quede constancia de la ultima trama 
                if  len(vali)==70:
                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[3]), 
                            "temp_supply_1": convertir_a_float(vali[4]),
                            "temp_supply_2": convertir_a_float(vali[5]),
                            "return_air": convertir_a_float(vali[6]), 
                            "evaporation_coil": convertir_a_float(vali[7]),
                            "condensation_coil": convertir_a_float(vali[8]),
                            "compress_coil_1": convertir_a_float(vali[9]),
                            "compress_coil_2": convertir_a_float(vali[10]), 
                            "ambient_air": convertir_a_float(vali[11]), 
                            "cargo_1_temp": convertir_a_float(vali[12]),
                            "cargo_2_temp": convertir_a_float(vali[13]), 
                            "cargo_3_temp": convertir_a_float(vali[14]), 
                            "cargo_4_temp": convertir_a_float(vali[15]), 
                            "relative_humidity": convertir_a_float(vali[16]), 
                            "avl": convertir_a_float(vali[17]), 
                            "suction_pressure": convertir_a_float(vali[18]), 
                            "discharge_pressure": convertir_a_float(vali[19]), 
                            "line_voltage": convertir_a_float(vali[20]), 
                            "line_frequency": convertir_a_float(vali[21]), 
                            "consumption_ph_1": convertir_a_float(vali[22]), 
                            "consumption_ph_2": convertir_a_float(vali[23]), 
                            "consumption_ph_3": convertir_a_float(vali[24]), 
                            "co2_reading": convertir_a_float(vali[25]), 
                            "o2_reading": convertir_a_float(vali[26]), 
                            "evaporator_speed": convertir_a_float(vali[27]), 
                            "condenser_speed": convertir_a_float(vali[28]),
                            "power_kwh": convertir_a_float(vali[29]),
                            "power_trip_reading": convertir_a_float(vali[30]),
                            "suction_temp": convertir_a_float(vali[31]),
                            "discharge_temp": convertir_a_float(vali[32]),
                            "supply_air_temp": convertir_a_float(vali[33]),
                            "return_air_temp": convertir_a_float(vali[34]),
                            "dl_battery_temp": convertir_a_float(vali[35]),
                            "dl_battery_charge": convertir_a_float(vali[36]),
                            "power_consumption": convertir_a_float(vali[37]),
                            "power_consumption_avg": convertir_a_float(vali[38]),
                            "alarm_present": convertir_a_float(vali[39]),
                            "capacity_load": convertir_a_float(vali[40]),
                            "power_state": convertir_a_float(vali[41]), 
                            "controlling_mode": vali[42],
                            "humidity_control": convertir_a_float(vali[43]),
                            "humidity_set_point": convertir_a_float(vali[44]),
                            "fresh_air_ex_mode": convertir_a_float(vali[45]),
                            "fresh_air_ex_rate": convertir_a_float(vali[46]),
                            "fresh_air_ex_delay": convertir_a_float(vali[47]),
                            "set_point_o2": convertir_a_float(vali[48]),
                            "set_point_co2": convertir_a_float(vali[49]),
                            "defrost_term_temp": convertir_a_float(vali[50]),
                            "defrost_interval": convertir_a_float(vali[51]),
                            "water_cooled_conde": convertir_a_float(vali[52]),
                            "usda_trip": convertir_a_float(vali[53]),
                            "evaporator_exp_valve": convertir_a_float(vali[54]),
                            "suction_mod_valve": convertir_a_float(vali[55]),
                            "hot_gas_valve": convertir_a_float(vali[56]),
                            "economizer_valve": convertir_a_float(vali[57]),
                            "ethylene": convertir_a_float(vali[58]),
                            "stateProcess": vali[59],
                            "stateInyection": vali[60],
                            "timerOfProcess": convertir_a_float(vali[61]),
                            "battery_voltage": convertir_a_float(vali[62]),
                            "power_trip_duration":convertir_a_float(vali[63]),
                            "modelo": vali[64],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": fecha_wonderful,
                            "telemetria_id": tele_wonderful,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[67]),
                            "inyeccion_hora": convertir_a_float(vali[68]),
                            "inyeccion_pwm": convertir_a_float(vali[69]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0
                        }
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    collectionMongoH.insert_one(objetoV)

                    base_novo = nombre_dispositivo+"_"+datazo
                    databaseMongo_NOVO = client[base_novo]
                    collectionMongo_NOVO = databaseMongo_NOVO.get_collection("madurador")
                    collectionMongo_NOVO.insert_one(objetoV)


                    objetoControl ={
                        "id":idProgre,
                        "telemetria_id":tele_wonderful,
                        "fecha":fecha_wonderful
                    }
                    if estadoC==1 :
                        #actualizar
                        collectionControl.update_one({"telemetria_id":tele_wonderful,},{"$set": {"id":idProgre,"fecha":fecha_wonderful}})
                    else :
                        #grabar
                        collectionControl.insert_one(objetoControl)
                        estadoC=1
                    curB = cnx.cursor()
                    update_old_salary = (
                    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                     " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                    curB.execute(update_old_salary, (fecha_wonderful, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                     objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                     objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                     objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                     objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                     objetoV['telemetria_id'],  ))
                    cnx.commit()
                    
    cnx.close()

    return idProgre




async def homologar_wonderful_zgru2008220() -> dict:
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]  
    collectionMongo = databaseMongo.get_collection("ZGRU2008220")
    trama=''
        # inicio de id para las telemetrias como referencias 
        #ZGRU1090804 -> 10000000000
        #ZGRU2009227 -> 11000000000
        #ZGRU2008220 -> 12000000000
        #ZGRU2232647 -> 13000000000
    idProgre = 12000000000
    #async for x in collectionMongo.find({"status":1}).sort("fecha",1).limit(10):
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):

        cad =x['data']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                if len(vali)==70:
                    print("listo pa insertar")
                    #aqui realizar la insercion de datos 
                    fecha_wonderful=x['fecha']
                    #telemetria_id de los dispositivos
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    tele_wonderful=260                    

                    objetoV = {
                        "id": idProgre,
                        "set_point": float(vali[3]), 
                        "temp_supply_1": float(vali[4]),
                        "temp_supply_2": float(vali[5]),
                        "return_air": float(vali[6]), 
                        "evaporation_coil": float(vali[7]),
                        "condensation_coil": float(vali[8]),
                        "compress_coil_1": float(vali[9]),
                        "compress_coil_2": float(vali[10]), 
                        "ambient_air": float(vali[11]), 
                        "cargo_1_temp": float(vali[12]),
                        "cargo_2_temp": float(vali[13]), 
                        "cargo_3_temp": float(vali[14]), 
                        "cargo_4_temp": float(vali[15]), 
                        "relative_humidity": float(vali[16]), 
                        "avl": float(vali[17]), 
                        "suction_pressure": float(vali[18]), 
                        "discharge_pressure": float(vali[19]), 
                        "line_voltage": float(vali[20]), 
                        "line_frequency": float(vali[21]), 
                        "consumption_ph_1": float(vali[22]), 
                        "consumption_ph_2": float(vali[23]), 
                        "consumption_ph_3": float(vali[24]), 
                        "co2_reading": float(vali[25]), 
                        "o2_reading": float(vali[26]), 
                        "evaporator_speed": float(vali[27]), 
                        "condenser_speed": float(vali[28]),
                        "power_kwh": float(vali[29]),
                        "power_trip_reading": float(vali[30]),
                        "suction_temp": float(vali[31]),
                        "discharge_temp": float(vali[32]),
                        "supply_air_temp": float(vali[33]),
                        "return_air_temp": float(vali[34]),
                        "dl_battery_temp": float(vali[35]),
                        "dl_battery_charge": float(vali[36]),
                        "power_consumption": float(vali[37]),
                        "power_consumption_avg": float(vali[38]),
                        "alarm_present": float(vali[39]),
                        "capacity_load": float(vali[40]),
                        "power_state": float(vali[41]), 
                        "controlling_mode": vali[42],
                        "humidity_control": float(vali[43]),
                        "humidity_set_point": float(vali[44]),
                        "fresh_air_ex_mode": float(vali[45]),
                        "fresh_air_ex_rate": float(vali[46]),
                        "fresh_air_ex_delay": float(vali[47]),
                        "set_point_o2": float(vali[48]),
                        "set_point_co2": float(vali[49]),
                        "defrost_term_temp": float(vali[50]),
                        "defrost_interval": float(vali[51]),
                        "water_cooled_conde": float(vali[52]),
                        "usda_trip": float(vali[53]),
                        "evaporator_exp_valve": float(vali[54]),
                        "suction_mod_valve": float(vali[55]),
                        "hot_gas_valve": float(vali[56]),
                        "economizer_valve": float(vali[57]),
                        "ethylene": float(vali[58]),
                        "stateProcess": vali[59],
                        "stateInyection": vali[60],
                        "timerOfProcess": float(vali[61]),
                        "battery_voltage": float(vali[62]),
                        "power_trip_duration":float(vali[63]),
                        "modelo": vali[64],
                        "latitud": 35.7396,
                        "longitud":  -119.238,
                        "created_at": fecha_wonderful,
                        "telemetria_id": tele_wonderful,
                        "inyeccion_etileno": 0,
                        "defrost_prueba": 0,
                        "ripener_prueba": 0,
                        "sp_ethyleno": int(vali[67]),
                        "inyeccion_hora": int(vali[68]),
                        "inyeccion_pwm": float(vali[69]),
                        "extra_1": 0,
                        "extra_2": 0,
                        "extra_3": 0,
                        "extra_4": 0,
                        "extra_5": 0
                    }

                    #actualizar en base de mysql
                    #insertaren bd mongodb 
                    #crear dat h_ZGRU1090804
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    #databaseMongoH = client['Homologar']  
                    #collectionMongoH = databaseMongoH.get_collection("ZGRU2009227")
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    #collectionMongoH.insert_one(objetoV)

    return baseD



async def homologar_wonderful_zgru2232647_2() -> dict:
    #ZGRU1090804 -> 33
    #ZGRU2009227 -> 259
    #ZGRU2008220 -> 260
    #ZGRU2232647 -> 258
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    tele_wonderful =258
    nombre_dispositivo='ZGRU2232647'
    controlTelemetria = await collectionControl.find_one({"telemetria_id":tele_wonderful})
    #print(controlTelemetria)
    idProgre = 13000000000
    factorBusqueda ={}
    estadoC=0
    print(controlTelemetria)
    if controlTelemetria :
        #print("tenemos datos")
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        print(fechaId)
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        print(factorBusqueda)
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection("ZGRU2232647")
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curA = cnx.cursor(buffered=True)
    curB = cnx.cursor(buffered=True)
    dataContenedor = curA.execute("SELECT * FROM contenedores WHERE nombre_contenedor='ZGRU2232647'")
    rows = curA.fetchall()
    conMysql =[]
    for row in rows :
        conMysql.append(row)
        print(row)

    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        print(x)
        fecha_wonderful=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                #aqui debe de guardarse en la tabal control para que quede constancia de la ultima trama 
                if  len(vali)==70:
                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[3]), 
                            "temp_supply_1": convertir_a_float(vali[4]),
                            "temp_supply_2": convertir_a_float(vali[5]),
                            "return_air": convertir_a_float(vali[6]), 
                            "evaporation_coil": convertir_a_float(vali[7]),
                            "condensation_coil": convertir_a_float(vali[8]),
                            "compress_coil_1": convertir_a_float(vali[9]),
                            "compress_coil_2": convertir_a_float(vali[10]), 
                            "ambient_air": convertir_a_float(vali[11]), 
                            "cargo_1_temp": convertir_a_float(vali[12]),
                            "cargo_2_temp": convertir_a_float(vali[13]), 
                            "cargo_3_temp": convertir_a_float(vali[14]), 
                            "cargo_4_temp": convertir_a_float(vali[15]), 
                            "relative_humidity": convertir_a_float(vali[16]), 
                            "avl": convertir_a_float(vali[17]), 
                            "suction_pressure": convertir_a_float(vali[18]), 
                            "discharge_pressure": convertir_a_float(vali[19]), 
                            "line_voltage": convertir_a_float(vali[20]), 
                            "line_frequency": convertir_a_float(vali[21]), 
                            "consumption_ph_1": convertir_a_float(vali[22]), 
                            "consumption_ph_2": convertir_a_float(vali[23]), 
                            "consumption_ph_3": convertir_a_float(vali[24]), 
                            "co2_reading": convertir_a_float(vali[25]), 
                            "o2_reading": convertir_a_float(vali[26]), 
                            "evaporator_speed": convertir_a_float(vali[27]), 
                            "condenser_speed": convertir_a_float(vali[28]),
                            "power_kwh": convertir_a_float(vali[29]),
                            "power_trip_reading": convertir_a_float(vali[30]),
                            "suction_temp": convertir_a_float(vali[31]),
                            "discharge_temp": convertir_a_float(vali[32]),
                            "supply_air_temp": convertir_a_float(vali[33]),
                            "return_air_temp": convertir_a_float(vali[34]),
                            "dl_battery_temp": convertir_a_float(vali[35]),
                            "dl_battery_charge": convertir_a_float(vali[36]),
                            "power_consumption": convertir_a_float(vali[37]),
                            "power_consumption_avg": convertir_a_float(vali[38]),
                            "alarm_present": convertir_a_float(vali[39]),
                            "capacity_load": convertir_a_float(vali[40]),
                            "power_state": convertir_a_float(vali[41]), 
                            "controlling_mode": vali[42],
                            "humidity_control": convertir_a_float(vali[43]),
                            "humidity_set_point": convertir_a_float(vali[44]),
                            "fresh_air_ex_mode": convertir_a_float(vali[45]),
                            "fresh_air_ex_rate": convertir_a_float(vali[46]),
                            "fresh_air_ex_delay": convertir_a_float(vali[47]),
                            "set_point_o2": convertir_a_float(vali[48]),
                            "set_point_co2": convertir_a_float(vali[49]),
                            "defrost_term_temp": convertir_a_float(vali[50]),
                            "defrost_interval": convertir_a_float(vali[51]),
                            "water_cooled_conde": convertir_a_float(vali[52]),
                            "usda_trip": convertir_a_float(vali[53]),
                            "evaporator_exp_valve": convertir_a_float(vali[54]),
                            "suction_mod_valve": convertir_a_float(vali[55]),
                            "hot_gas_valve": convertir_a_float(vali[56]),
                            "economizer_valve": convertir_a_float(vali[57]),
                            "ethylene": convertir_a_float(vali[58]),
                            "stateProcess": vali[59],
                            "stateInyection": vali[60],
                            "timerOfProcess": convertir_a_float(vali[61]),
                            "battery_voltage": convertir_a_float(vali[62]),
                            "power_trip_duration":convertir_a_float(vali[63]),
                            "modelo": vali[64],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": fecha_wonderful,
                            "telemetria_id": tele_wonderful,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[67]),
                            "inyeccion_hora": convertir_a_float(vali[68]),
                            "inyeccion_pwm": convertir_a_float(vali[69]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0
                        }
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")  
                    collectionMongoH.insert_one(objetoV)
                    
                    base_novo = nombre_dispositivo+"_"+datazo
                    databaseMongo_NOVO = client[base_novo]
                    collectionMongo_NOVO = databaseMongo_NOVO.get_collection("madurador")
                    collectionMongo_NOVO.insert_one(objetoV)
                    objetoControl ={
                        "id":idProgre,
                        "telemetria_id":tele_wonderful,
                        "fecha":fecha_wonderful
                    }
                    if estadoC==1 :
                        #actualizar
                        collectionControl.update_one({"telemetria_id":tele_wonderful,},{"$set": {"id":idProgre,"fecha":fecha_wonderful}})
                    else :
                        #grabar
                        collectionControl.insert_one(objetoControl)
                        estadoC=1
                    curB = cnx.cursor()
                    update_old_salary = (
                    "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                    ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                     " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                    curB.execute(update_old_salary, (fecha_wonderful, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                     objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                     objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                     objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                     objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                     objetoV['telemetria_id'],  ))
                    cnx.commit()
    cnx.close()
 
    return idProgre


#starcool_ZGRU1092515
async def starcool_ZGRU1092515() -> dict:
    return "oli"
    

async def homologar_wonderful_zgru2232647() -> dict:
    datazo = obtener_mes_y_anio_actual()
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]  
    collectionMongo = databaseMongo.get_collection("ZGRU2232647")
    trama=''
        # inicio de id para las telemetrias como referencias 
        #ZGRU1090804 -> 10000000000
        #ZGRU2009227 -> 11000000000
        #ZGRU2008220 -> 12000000000
        #ZGRU2232647 -> 13000000000
    idProgre = 13000000000
    #async for x in collectionMongo.find({"status":1}).sort("fecha",1).limit(10):
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):

        cad =x['data']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                if len(vali)==70:
                    print("listo pa insertar")
                    #aqui realizar la insercion de datos 
                    fecha_wonderful=x['fecha']
                    #telemetria_id de los dispositivos
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    tele_wonderful=258                    

                    objetoV = {
                        "id": idProgre,
                        "set_point": float(vali[3]), 
                        "temp_supply_1": float(vali[4]),
                        "temp_supply_2": float(vali[5]),
                        "return_air": float(vali[6]), 
                        "evaporation_coil": float(vali[7]),
                        "condensation_coil": float(vali[8]),
                        "compress_coil_1": float(vali[9]),
                        "compress_coil_2": float(vali[10]), 
                        "ambient_air": float(vali[11]), 
                        "cargo_1_temp": float(vali[12]),
                        "cargo_2_temp": float(vali[13]), 
                        "cargo_3_temp": float(vali[14]), 
                        "cargo_4_temp": float(vali[15]), 
                        "relative_humidity": float(vali[16]), 
                        "avl": float(vali[17]), 
                        "suction_pressure": float(vali[18]), 
                        "discharge_pressure": float(vali[19]), 
                        "line_voltage": float(vali[20]), 
                        "line_frequency": float(vali[21]), 
                        "consumption_ph_1": float(vali[22]), 
                        "consumption_ph_2": float(vali[23]), 
                        "consumption_ph_3": float(vali[24]), 
                        "co2_reading": float(vali[25]), 
                        "o2_reading": float(vali[26]), 
                        "evaporator_speed": float(vali[27]), 
                        "condenser_speed": float(vali[28]),
                        "power_kwh": float(vali[29]),
                        "power_trip_reading": float(vali[30]),
                        "suction_temp": float(vali[31]),
                        "discharge_temp": float(vali[32]),
                        "supply_air_temp": float(vali[33]),
                        "return_air_temp": float(vali[34]),
                        "dl_battery_temp": float(vali[35]),
                        "dl_battery_charge": float(vali[36]),
                        "power_consumption": float(vali[37]),
                        "power_consumption_avg": float(vali[38]),
                        "alarm_present": float(vali[39]),
                        "capacity_load": float(vali[40]),
                        "power_state": float(vali[41]), 
                        "controlling_mode": vali[42],
                        "humidity_control": float(vali[43]),
                        "humidity_set_point": float(vali[44]),
                        "fresh_air_ex_mode": float(vali[45]),
                        "fresh_air_ex_rate": float(vali[46]),
                        "fresh_air_ex_delay": float(vali[47]),
                        "set_point_o2": float(vali[48]),
                        "set_point_co2": float(vali[49]),
                        "defrost_term_temp": float(vali[50]),
                        "defrost_interval": float(vali[51]),
                        "water_cooled_conde": float(vali[52]),
                        "usda_trip": float(vali[53]),
                        "evaporator_exp_valve": float(vali[54]),
                        "suction_mod_valve": float(vali[55]),
                        "hot_gas_valve": float(vali[56]),
                        "economizer_valve": float(vali[57]),
                        "ethylene": float(vali[58]),
                        "stateProcess": vali[59],
                        "stateInyection": vali[60],
                        "timerOfProcess": float(vali[61]),
                        "battery_voltage": float(vali[62]),
                        "power_trip_duration":float(vali[63]),
                        "modelo": vali[64],
                        "latitud": 35.7396,
                        "longitud":  -119.238,
                        "created_at": fecha_wonderful,
                        "telemetria_id": tele_wonderful,
                        "inyeccion_etileno": 0,
                        "defrost_prueba": 0,
                        "ripener_prueba": 0,
                        "sp_ethyleno": int(vali[67]),
                        "inyeccion_hora": int(vali[68]),
                        "inyeccion_pwm": float(vali[69]),
                        "extra_1": 0,
                        "extra_2": 0,
                        "extra_3": 0,
                        "extra_4": 0,
                        "extra_5": 0
                    }

                    #actualizar en base de mysql
                    #insertaren bd mongodb 
                    #crear dat h_ZGRU1090804
                    #ZGRU1090804 -> 33
                    #ZGRU2009227 -> 259
                    #ZGRU2008220 -> 260
                    #ZGRU2232647 -> 258
                    #databaseMongoH = client['Homologar']  
                    #collectionMongoH = databaseMongoH.get_collection("ZGRU2009227")
                    databaseMongoH = client['ztrack_ja']  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    #collectionMongoH.insert_one(objetoV)

    return baseD



async def homologar_datos_wonderful(notificacion_data: dict) -> dict :
    #ZGRU1090804 -> 33
    #ZGRU2009227 -> 259
    #ZGRU2008220 -> 260
    #ZGRU2232647 -> 258
    #notificacion_data['mes']
    #datazo = obtener_mes_y_anio_actual()
    datazo = notificacion_data['mes']
    baseD = "WONDERFUL_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("controlx")
    #tele_wonderful =258
    tele_wonderful =notificacion_data['telemetria_id']
    #nombre_dispositivo='ZGRU2232647'
    nombre_dispositivo=notificacion_data['device']
    controlTelemetria = await collectionControl.find_one({"telemetria_id":tele_wonderful})
    #print(controlTelemetria)
    #idProgre = 13000000000
    idProgre = notificacion_data['id_g']
    factorBusqueda ={}
    estadoC=0
    print(controlTelemetria)
    if controlTelemetria :
        #print("tenemos datos")
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        print(fechaId)
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        print(factorBusqueda)
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection(nombre_dispositivo)
    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        print(x)
        fecha_wonderful=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f1 =cad.split('|')
        p1=f1[0]
        f2=p1.split(',')
        print(cad)
        if f2[0]=='1CR1':
            trama=''
            trama =trama+f1[0]
            p2=f1[1]
            datote =p2.split('*')
            trama=trama+datote[0]
            print('vamo construyendo 1')
        if f2[0]=='1CR2':
            if trama!='':
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print('vamo construyendo 2')
        if f2[0]=='1CR3':
            if trama!='':
                idProgre=idProgre+1
                p2=f1[1]
                datote =p2.split('*')
                trama=trama+datote[0]
                print(trama)
                vali = trama.split(',')
                #aqui debe de guardarse en la tabal control para que quede constancia de la ultima trama 
                if  len(vali)==70:

                    objetoV = {
                            "id": idProgre,
                            "set_point": convertir_a_float(vali[3]), 
                            "temp_supply_1": convertir_a_float(vali[4]),
                            "temp_supply_2": convertir_a_float(vali[5]),
                            "return_air": convertir_a_float(vali[6]), 
                            "evaporation_coil": convertir_a_float(vali[7]),
                            "condensation_coil": convertir_a_float(vali[8]),
                            "compress_coil_1": convertir_a_float(vali[9]),
                            "compress_coil_2": convertir_a_float(vali[10]), 
                            "ambient_air": convertir_a_float(vali[11]), 
                            "cargo_1_temp": convertir_a_float(vali[12]),
                            "cargo_2_temp": convertir_a_float(vali[13]), 
                            "cargo_3_temp": convertir_a_float(vali[14]), 
                            "cargo_4_temp": convertir_a_float(vali[15]), 
                            "relative_humidity": convertir_a_float(vali[16]), 
                            "avl": convertir_a_float(vali[17]), 
                            "suction_pressure": convertir_a_float(vali[18]), 
                            "discharge_pressure": convertir_a_float(vali[19]), 
                            "line_voltage": convertir_a_float(vali[20]), 
                            "line_frequency": convertir_a_float(vali[21]), 
                            "consumption_ph_1": convertir_a_float(vali[22]), 
                            "consumption_ph_2": convertir_a_float(vali[23]), 
                            "consumption_ph_3": convertir_a_float(vali[24]), 
                            "co2_reading": convertir_a_float(vali[25]), 
                            "o2_reading": convertir_a_float(vali[26]), 
                            "evaporator_speed": convertir_a_float(vali[27]), 
                            "condenser_speed": convertir_a_float(vali[28]),
                            "power_kwh": convertir_a_float(vali[29]),
                            "power_trip_reading": convertir_a_float(vali[30]),
                            "suction_temp": convertir_a_float(vali[31]),
                            "discharge_temp": convertir_a_float(vali[32]),
                            "supply_air_temp": convertir_a_float(vali[33]),
                            "return_air_temp": convertir_a_float(vali[34]),
                            "dl_battery_temp": convertir_a_float(vali[35]),
                            "dl_battery_charge": convertir_a_float(vali[36]),
                            "power_consumption": convertir_a_float(vali[37]),
                            "power_consumption_avg": convertir_a_float(vali[38]),
                            "alarm_present": convertir_a_float(vali[39]),
                            "capacity_load": convertir_a_float(vali[40]),
                            "power_state": convertir_a_float(vali[41]), 
                            "controlling_mode": vali[42],
                            "humidity_control": convertir_a_float(vali[43]),
                            "humidity_set_point": convertir_a_float(vali[44]),
                            "fresh_air_ex_mode": convertir_a_float(vali[45]),
                            "fresh_air_ex_rate": convertir_a_float(vali[46]),
                            "fresh_air_ex_delay": convertir_a_float(vali[47]),
                            "set_point_o2": convertir_a_float(vali[48]),
                            "set_point_co2": convertir_a_float(vali[49]),
                            "defrost_term_temp": convertir_a_float(vali[50]),
                            "defrost_interval": convertir_a_float(vali[51]),
                            "water_cooled_conde": convertir_a_float(vali[52]),
                            "usda_trip": convertir_a_float(vali[53]),
                            "evaporator_exp_valve": convertir_a_float(vali[54]),
                            "suction_mod_valve": convertir_a_float(vali[55]),
                            "hot_gas_valve": convertir_a_float(vali[56]),
                            "economizer_valve": convertir_a_float(vali[57]),
                            "ethylene": convertir_a_float(vali[58]),
                            "stateProcess": vali[59],
                            "stateInyection": vali[60],
                            "timerOfProcess": convertir_a_float(vali[61]),
                            "battery_voltage": convertir_a_float(vali[62]),
                            "power_trip_duration":convertir_a_float(vali[63]),
                            "modelo": vali[64],
                            "latitud": 35.7396,
                            "longitud":  -119.238,
                            "created_at": fecha_wonderful,
                            "telemetria_id": tele_dispositivo,
                            "inyeccion_etileno": 0,
                            "defrost_prueba": 0,
                            "ripener_prueba": 0,
                            "sp_ethyleno": convertir_a_float(vali[67]),
                            "inyeccion_hora": convertir_a_float(vali[68]),
                            "inyeccion_pwm": convertir_a_float(vali[69]),
                            "extra_1": 0,
                            "extra_2": 0,
                            "extra_3": 0,
                            "extra_4": 0,
                            "extra_5": 0
                        }
                    #buscamos la base de datos 
                    #nombre_bd_wonderful = "P_"+nombre_dispositivo +datazo
                    nombre_bd_wonderful = nombre_dispositivo +"_"+datazo

                    #databaseMongoH = client['ztrack_ja']  
                    databaseMongoH = client[nombre_bd_wonderful]  
                    collectionMongoH = databaseMongoH.get_collection("madurador")
                    collectionMongoH.insert_one(objetoV)
                    objetoControl ={
                        "id":idProgre,
                        "telemetria_id":tele_wonderful,
                        "fecha":fecha_wonderful
                    }
                    if estadoC==1 :
                        #actualizar
                        collectionControl.update_one({"telemetria_id":tele_wonderful,},{"$set": {"id":idProgre,"fecha":fecha_wonderful}})
                    else :
                        #grabar
                        collectionControl.insert_one(objetoControl)
                        estadoC=1
    return idProgre


