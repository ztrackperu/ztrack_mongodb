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

def obtener_mes_y_anio_actual():
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()
    
    # Obtener el mes y el año
    mes_actual = fecha_actual.month
    anio_actual = fecha_actual.year
    
    # Formatear la cadena mes_año
    mes_anio_str = f"{mes_actual}_{anio_actual}"
    return mes_anio_str

def validarON(cadena):
    # Validar si la cadena es numérica
    try:
        valor_numerico = float(cadena)
        return float(valor_numerico)
    except ValueError:
        pass
    
    # Si la cadena no es numérica, verificar si comienza con "TD:"
    if cadena.startswith("TD:"):
        # Quitar "TD:" del principio y retornar el resto de la cadena
        return cadena[3:]
    else:
        # Retornar 'NA' si no es numérica y no comienza con "TD:"
        return 'NA'

def validar_dato(dato):
    if isinstance(dato, str):
        dato = dato.strip()  # Eliminamos espacios en blanco al inicio y al final
    
    if isinstance(dato, str) and dato.lower() == 'na':
        return None
    try:
        return float(dato)
    except ValueError:
        return None

def procesaObjeto(trama,idProgre,fecha_wonderful,tele_wonderful):
    vali = trama.split(',')
    objetoV = {
        "id": idProgre,
        "set_point": validar_dato(vali[3]), 
        "temp_supply_1": validar_dato(vali[4]),
        "temp_supply_2": validar_dato(vali[5]),
        "return_air": validar_dato(vali[6]), 
        "evaporation_coil": validar_dato(vali[7]),
        "condensation_coil": validar_dato(vali[8]),
        "compress_coil_1": validar_dato(vali[9]),
        "compress_coil_2": validar_dato(vali[10]), 
        "ambient_air": validar_dato(vali[11]), 
        "cargo_1_temp": validar_dato(vali[12]),
        "cargo_2_temp": validar_dato(vali[13]), 
        "cargo_3_temp": validar_dato(vali[14]), 
        "cargo_4_temp": validar_dato(vali[15]), 
        "relative_humidity": validar_dato(vali[16]), 
        "avl": validar_dato(vali[17]), 
        "suction_pressure": validar_dato(vali[18]), 
        "discharge_pressure": validar_dato(vali[19]), 
        "line_voltage": validar_dato(vali[20]), 
        "line_frequency": validar_dato(vali[21]), 
        "consumption_ph_1": validar_dato(vali[22]), 
        "consumption_ph_2": validar_dato(vali[23]), 
        "consumption_ph_3": validar_dato(vali[24]), 
        "co2_reading": validar_dato(vali[25]), 
        "o2_reading": validar_dato(vali[26]), 
        "evaporator_speed": validar_dato(vali[27]), 
        "condenser_speed": validar_dato(vali[28]),
        "power_kwh": validar_dato(vali[29]),
        "power_trip_reading": validar_dato(vali[30]),
        "suction_temp": validar_dato(vali[31]),
        "discharge_temp": validar_dato(vali[32]),
        "supply_air_temp": validar_dato(vali[33]),
        "return_air_temp": validar_dato(vali[34]),
        "dl_battery_temp": validar_dato(vali[35]),
        "dl_battery_charge": validar_dato(vali[36]),
        "power_consumption": validar_dato(vali[37]),
        "power_consumption_avg": validar_dato(vali[38]),
        "alarm_present": validar_dato(vali[39]),
        "capacity_load": validar_dato(vali[40]),
        "power_state": validar_dato(validarON(vali[41])), 
        "controlling_mode": validar_dato(vali[42]),
        "humidity_control": validar_dato(vali[43]),
        "humidity_set_point": validar_dato(vali[44]),
        "fresh_air_ex_mode": validar_dato(vali[45]),
        "fresh_air_ex_rate": validar_dato(vali[46]),
        "fresh_air_ex_delay": validar_dato(vali[47]),
        "set_point_o2": validar_dato(vali[48]),
        "set_point_co2": validar_dato(vali[49]),
        "defrost_term_temp": validar_dato(vali[50]),
        "defrost_interval": validar_dato(vali[51]),
        "water_cooled_conde": validar_dato(vali[52]),
        "usda_trip": validar_dato(vali[53]),
        "evaporator_exp_valve": validar_dato(vali[54]),
        "suction_mod_valve": validar_dato(vali[55]),
        "hot_gas_valve": validar_dato(vali[56]),
        "economizer_valve": validar_dato(vali[57]),
        "ethylene": validar_dato(vali[58]),
        "stateProcess": validar_dato(vali[59]),
        "stateInyection": validar_dato(vali[60]),
        "timerOfProcess": validar_dato(vali[61]),
        "battery_voltage": validar_dato(vali[62]),
        "power_trip_duration":validar_dato(vali[63]),
        "modelo": validar_dato(vali[64]),
        "latitud": 35.7396,
        "longitud":  -119.238,
        "created_at": fecha_wonderful,
        "telemetria_id": tele_wonderful,
        "inyeccion_etileno": 0,
        "defrost_prueba": 0,
        "ripener_prueba": 0,
        "sp_ethyleno": validar_dato(vali[67]),
        "inyeccion_hora": validar_dato(vali[68]),
        "inyeccion_pwm": validar_dato(vali[69]),
        "extra_1": 0,
        "extra_2": 0,
        "extra_3": 0,
        "extra_4": 0,
        "extra_5": 0
    }
    return objetoV

def diferencia_fecha(fecha1, fecha2):
    # Convertir las cadenas de fecha en objetos datetime
    try:
        fecha1 = datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
        fecha2 = datetime.strptime(fecha2, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Las fechas deben estar en formato 'YYYY-MM-DD HH:MM:SS'")
    # Calcular la diferencia entre las fechas
    diferencia = abs(fecha1 - fecha2)
    
    # Comparar la diferencia con 30 segundos
    if diferencia > timedelta(seconds=30):
        return 1
    else:
        return 0
    

def diferencia_fecha2(fecha1, fecha2):

    # Calcular la diferencia entre las fechas
    diferencia = abs(fecha1 - fecha2)  
    # Comparar la diferencia con 30 segundos
    if diferencia > timedelta(seconds=30):
        return 1
    else:
        return 0

def generar_cadena_extendida(cadena_original, nuevas_posiciones, numero_elementos):
    # Convertimos la cadena original en una lista separada por comas
    elementos = cadena_original.split(',')  
    # Creamos una lista inicial con 'NA' en todas las posiciones según el número de elementos deseado
    resultado = ['NA'] * numero_elementos
    # Insertamos los elementos en las nuevas posiciones especificadas
    for posicion, elemento in zip(nuevas_posiciones, elementos):
        resultado[posicion - 1] = elemento  # Restamos 1 porque las posiciones son 1-indexed
    # Convertimos la lista resultado de nuevo a cadena separada por comas y la retornamos
    return ','.join(resultado)

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

#procesamiento de informacion 


# Ejemplo de uso:
#cadena_original = "COD,PAR,POR,TRA,JOB,TEL,SPU"
#nuevas_posiciones = [1, 4, 7, 8, 13, 21, 22]
#numero_elementos = 25

#resultado = generar_cadena_extendida(cadena_original, nuevas_posiciones, numero_elementos)
#print(resultado)


async def homologar_hortifruit_123321() -> dict:
    datazo = obtener_mes_y_anio_actual()
    baseD = "HORTIFRUIT_"+datazo
    databaseMongo = client[baseD]  
    #implementar logica HORTIFRUIT + codigo capicua 
    collectionMongo = databaseMongo.get_collection("123321")
    trama=''
        # inicio de id para las telemetrias como referencias 
        # 123321 -> 14000000000
        # 234432 -> 15000000000
        # 345543 -> 16000000000
        # 456654 -> 17000000000
        # 567765 -> 18000000000
    idProgre = 14000000000
    #async for x in collectionMongo.find({"status":1}).sort("fecha",1).limit(10):
    proceso =0
    fecha_anterior=None
    async for x in collectionMongo.find({"status":1}).sort("fecha",1):
        cad =x['data']
        nuevas_posiciones = [65,2,1,3,42,13,14,15,16,5,7,4,40]
        numero_elementos = 70
        fecha_dato=x['fecha']
        tele_dato=25800 
        nova_cadena = generar_cadena_extendida(cad, nuevas_posiciones, numero_elementos)
        print(nova_cadena)
        objeto_generado = procesaObjeto(nova_cadena,idProgre,fecha_dato,tele_dato)
        print(objeto_generado)

        databaseMongoH = client['homologado_ecuador']  
        collectionMongoH = databaseMongoH.get_collection("123321")

        if proceso==0:
            fecha_anterior=x['fecha']
            collectionMongoH.insert_one(objeto_generado)
            print('insertar')
            proceso=1
        else:
            #dato proceso de fecha
            if diferencia_fecha2(fecha_anterior, x['fecha'])==1:
            #if (x['fecha']-fecha_anterior)>30 :
                collectionMongoH.insert_one(objeto_generado)
                print('diferencia mayor a 30 segundos')
            proceso=0
    return baseD
