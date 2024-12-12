import json
import mysql.connector
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from server.generico.base_conexion import BaseConexion
from dateutil.relativedelta import relativedelta

db_connection = mysql.connector.connect(
    host= "localhost",
    user= "ztrack2023",
    passwd= "lpmp2018",
    database="zgroupztrack"
)


def Get_Number_starcool(vector,index,Bytes):
    length = len(vector)
    index = index - 1
    index = index * 2
    Bytes = Bytes * 2
    Cnt_Bytes = 0
    numero = 0
    for i in range(0,length):
        if(i >= index):
            if(Cnt_Bytes < Bytes):
                numero = numero << 4
                numero = numero | Caracter_Hex_starcool(vector[i])
                Cnt_Bytes = Cnt_Bytes + 1
    return numero

def Caracter_Hex_starcool(val):
    if val == '0':
        return 0x0
    if val == '1':
        return 0x1
    if val == '2':
        return 0x2
    if val == '3':
        return 0x3
    if val == '4':
        return 0x4
    if val == '5':
        return 0x5
    if val == '6':
        return 0x6
    if val == '7':
        return 0x7
    if val == '8':
        return 0x8
    if val == '9':
        return 0x9    
    if val == 'a' or val == 'A':
        return 0xA
    if val == 'b' or val == 'B':
        return 0xB
    if val == 'c' or val == 'C':
        return 0xC
    if val == 'd' or val == 'D':
        return 0xD
    if val == 'e' or val == 'E':
        return 0xE
    if val == 'f' or val == 'F':
        return 0xF

def Valor_Convertido_starcool(valve):
    if(valve <= 0xFF):
        valve = 0xC000 | valve
    aux = valve
    signo = 0
    aux = aux & 0xF000
    if(aux == 0xF000):
        #print("Es negativo")
        signo = 1
        valve = valve - 0xF000
    else:
        valve = valve - 0xC000
    valve = valve & 0xFFFF
    valve = valve >> 4
    if(signo==1):
        valve = 0x100 - valve
    valve = valve / 4.0
    if(signo == 1):
        valve = -valve
    return valve

#nombre = ["Set Point", "Supply 1 temp","Return temp","Evaporator temp","Ambient temp","Supply 2 temp"]

def resultados_starcool(cadena): 
    set_point = Get_Number_starcool(cadena,1,2)
    set_point = Valor_Convertido_starcool(set_point)

    supply_1 = Get_Number_starcool(cadena,3,2)
    supply_1 = Valor_Convertido_starcool(supply_1)

    retorno = Get_Number_starcool(cadena,5,2)
    retorno = Valor_Convertido_starcool(retorno)

    evap = Get_Number_starcool(cadena,7,2)
    evap = Valor_Convertido_starcool(evap)

    ambien = Get_Number_starcool(cadena,9,2)
    ambien = Valor_Convertido_starcool(ambien)

    supply_2 = Get_Number_starcool(cadena,11,2)
    supply_2 = Valor_Convertido_starcool(supply_2)

    return [set_point,supply_1,retorno,evap,ambien,supply_2]

#print(nombre)
#print(resultados_starcool(str))


def obtener_mes_ano_anterior():
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Restar un mes
    #fecha_anterior = fecha_actual - relativedelta(months=1)
    fecha_anterior = fecha_actual 

    # Formatear mes y año anterior en el formato deseado
    repositorio = f"S_dispositivos_{fecha_anterior.strftime('%m')}_{fecha_anterior.strftime('%Y')}"
    return repositorio

def obtener_mes_ano_anterior_imei(imei):
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Restar un mes
    #fecha_anterior = fecha_actual - relativedelta(months=1)
    fecha_anterior = fecha_actual 
    # Formatear mes y año anterior en el formato deseado
    repositorio = f"S_{imei}_{fecha_anterior.strftime('%m')}_{fecha_anterior.strftime('%Y')}"
    return repositorio


async def proceso_control_nestle()-> dict : 
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    data_dispositivo = []
    curDispositivos = cnx.cursor(buffered=True)
    curConteB = cnx.cursor(buffered=True)
    consulta_dispositivos = ("SELECT * FROM contenedores where empresa_id=70 and estado=1")
    curDispositivos.execute(consulta_dispositivos)
    for z in curDispositivos:
        data_dispositivo.append(z)
        print("******")
        print(z[1])
        print("******")
        print(z[4])
        print("******")
        print(z[8])

    
    #id_obtenido = data_ultima[0][0] +1
    return data_dispositivo




async def homologar_api_starcool_general() -> dict:
    datazo = BaseConexion.obtener_mes_y_anio_actual()
    base_anterior = obtener_mes_ano_anterior()
    print(datazo)
    print(base_anterior)
    baseD = "ZTRACK_API"
    databaseMongo = client[baseD]
    collectionImei =databaseMongo.get_collection(base_anterior)
    imeis = []
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curConte = cnx.cursor(buffered=True)
    curConteB = cnx.cursor(buffered=True)
    async for x in collectionImei.find():
        imeis.append(x['imei'])
        consulta_telemetria = ("SELECT * FROM telemetrias WHERE imei=%s and estado=1")
        #query_contenedor = curConte.execute(consulta_contenedor,(str(x['imei']),))
        identi = "S"+str(x['imei'])
        curConte.execute(consulta_telemetria,(identi,))
        data_telemtria = []
        data_ultima = []
        print("-------------------")
        print(x['imei'])
        print("-------------------")
        for y in curConte:
            data_telemtria.append(y)
        if len(data_telemtria)>0 :
            id_obtenido = data_telemtria[0][0]
        else : 
            consulta_ultimo_id_tele = ("SELECT id FROM telemetrias  order by id desc  limit 1  ")
            curConte.execute(consulta_ultimo_id_tele)
            for z in curConte:
                data_ultima.append(z)
            id_obtenido = data_ultima[0][0] +1
            #creo el dispostivo en cuestion 
            insert_new_telemetria = ("INSERT INTO telemetrias (id, numero_telefono, imei) "
                "VALUES (%s, %s, %s)")
            curConteB.execute(insert_new_telemetria,(id_obtenido, identi, identi))
        print(id_obtenido)
        #consulto a la tabla contenedores por telemetria_id
        consulta_contenedor = ("SELECT * FROM contenedores WHERE telemetria_id=%s and estado=1")
        curConte.execute(consulta_contenedor,(id_obtenido,))
        data_contenedor = []
        for y1 in curConte:
            data_contenedor.append(y1)
        if len(data_contenedor)==0 :
            #cremoas contenedor con descripcion 
            insert_new_contenedor = ("INSERT INTO contenedores (nombre_contenedor, tipo, telemetria_id) "
                "VALUES (%s, %s, %s)")
            curConteB.execute(insert_new_contenedor,(identi, "Madurador", id_obtenido))
        

        #leer la tabla correspondiente y de froma masiva importar 
        base_imei =obtener_mes_ano_anterior_imei(str(x['imei']))
        collection_especifica =databaseMongo.get_collection(base_imei)
        prueba_collection =databaseMongo.get_collection("prueba_colect")
        ij = 240000
        fecha_t ="2024-12-11T13:55:54"
        fecha_ok = datetime.fromisoformat(fecha_t)+timedelta(minutes=0)
        factorBusqueda ={"fecha":{"$gt":fecha_ok}}
        async for notificacion in collection_especifica.find(factorBusqueda,{"_id":0}).sort({"fecha":1}):
            print("********")
            captura_datos = notificacion['d01']
            if len(captura_datos)>100  :
                #print("bueno")
                row = resultados_starcool(captura_datos[6:])
                print(row)
                #['Set Point', 'Supply 1 temp', 'Return temp', 'Evaporator temp', 'Ambient temp', 'Supply 2 temp']
                objetoV = {
                    "id": ij,
                    "set_point": row[0], 
                    "temp_supply_1": row[1],
                    "temp_supply_2": row[5],
                    "return_air": row[2], 
                    "evaporation_coil": row[3],
                    "condensation_coil": 0.00,
                    "compress_coil_1": None,
                    "compress_coil_2": 0.00, 
                    "ambient_air": row[4], 
                    "cargo_1_temp": 0.00,
                    "cargo_2_temp": 0.00, 
                    "cargo_3_temp": 0.00, 
                    "cargo_4_temp": 0.00, 
                    "relative_humidity": None, 
                    "avl": 0.00, 
                    "suction_pressure": 0.00, 
                    "discharge_pressure": 0.00, 
                    "line_voltage": 0.00, 
                    "line_frequency": 0.00, 
                    "consumption_ph_1": 0.00, 
                    "consumption_ph_2": 0.00, 
                    "consumption_ph_3": 0.00, 
                    "co2_reading": 0.00, 
                    "o2_reading": 0.00, 
                    "evaporator_speed": 0.00, 
                    "condenser_speed": 0.00,
                    "power_kwh": 0.00,
                    "power_trip_reading": 0.00,
                    "suction_temp": 0.00,
                    "discharge_temp": 0.00,
                    "supply_air_temp": 0.00,
                    "return_air_temp": 0.00,
                    "dl_battery_temp": 0.00,
                    "dl_battery_charge": 0.00,
                    "power_consumption": 0.00,
                    "power_consumption_avg": 0.00,
                    "alarm_present": 0.00,
                    "capacity_load": 0.00,
                    "power_state": 1, 
                    "controlling_mode": 1,
                    "humidity_control": 0.00,
                    "humidity_set_point": 0.00,
                    "fresh_air_ex_mode": 0.00,
                    "fresh_air_ex_rate": 0.00,
                    "fresh_air_ex_delay": 0.00,
                    "set_point_o2": 0.00,
                    "set_point_co2": 0.00,
                    "defrost_term_temp": 0.00,
                    "defrost_interval": 0.00,
                    "water_cooled_conde": 0.00,
                    "usda_trip": 0.00,
                    "evaporator_exp_valve": 0.00,
                    "suction_mod_valve": 0.00,
                    "hot_gas_valve": 0.00,
                    "economizer_valve": 0.00,
                    "ethylene": 0.00,
                    "stateProcess": 0.00,
                    "stateInyection": 0.00,
                    "timerOfProcess": 0.00,
                    "battery_voltage": 0.00,
                    "power_trip_duration":0.00,
                    "modelo": 0.00,
                    "latitud": 0.00,
                    "longitud":  0.00,
                    "created_at": notificacion['fecha'],
                    "telemetria_id": id_obtenido,
                    "inyeccion_etileno": 0,
                    "defrost_prueba": 0,
                    "ripener_prueba": 0,
                    "sp_ethyleno": 0.00,
                    "inyeccion_hora": 0.00,
                    "inyeccion_pwm": 0.00,
                    "extra_1": 0,
                    "extra_2": 0,
                    "extra_3": 0,
                    "extra_4": 0,
                    "extra_5": 0
                }
                ij+=1
                databaseMongoH = client['ztrack_ja']  
                #collectionMongoH = databaseMongoH.get_collection("madurador_starcool")
                collectionMongoH = databaseMongoH.get_collection("madurador")

                collectionMongoH.insert_one(objetoV)
                print(objetoV)
                curB = cnx.cursor()
                update_old_salary = (
                "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                    " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                curB.execute(update_old_salary, (objetoV['created_at'], objetoV['set_point'],objetoV['temp_supply_1'], 
                                                    objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                    objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                    objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                    objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                    objetoV['telemetria_id'],  ))

                cnx.commit()



            else :
                print("malito")
            #print(notificacion['d01'])

            #print("********")    

    return imeis
