import json
import asyncio
from contextlib import asynccontextmanager
import mysql.connector
from mysql.connector import pooling
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from server.generico.base_conexion import BaseConexion
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Optional

db_connection = mysql.connector.connect(
    host= "localhost",
    user= "ztrack2023",
    passwd= "lpmp2018",
    database="zgroupztrack"
)


def Get_Number_starcool_one(vector,index,Bytes):
    inicio = int(index*Bytes)
    fin = int((index+1)*Bytes)
    trama_recortada = vector[inicio:fin]
    valor_decimal = int(trama_recortada, 16)
    resultado = valor_decimal / 10
    return resultado


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

    #opciones de datos o2 setpoint , o2 , co2 setpoint , co2  : 35,36,37,38
    o2_set = Get_Number_starcool_one(cadena,34,2)

    o2_reading = Get_Number_starcool_one(cadena,35,2)
    co2_set = Get_Number_starcool_one(cadena,36,2)
    co2_reading = Get_Number_starcool_one(cadena,37,2)

    return [set_point,supply_1,retorno,evap,ambien,supply_2 ,o2_set,o2_reading,co2_set,co2_reading]

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

    #consultar a coleccion "control_starcool"
    collectionStarControl =databaseMongo.get_collection("control_starcool")
    controlStarCool = []
    async for xy in collectionStarControl.find():
        controlStarCool.append(xy)
    if controlStarCool :
        print("*******")
        print(controlStarCool[0]['ij'])
        print("*******")
        print(controlStarCool[0]['fecha_t'])
    else : 
        print("sin datos encontrados")
        #insertar datos 
        objetoS = {
            "ij" :250000,
            "fecha_t" :"2024-12-11T17:35:54",
            "control" :1
        }
        collectionStarControl.insert_one(objetoS)
        print("guarddado en starcool control")




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
          
        #ij = 241000
        ij =controlStarCool[0]['ij']
        #fecha_t ="2024-12-11T23:35:54"
        fecha_t = controlStarCool[0]['fecha_t']
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
                   # return [set_point,supply_1,retorno,evap,ambien,supply_2 ,o2_set,o2_reading,co2_set,co2_reading]

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
                    "co2_reading": row[9], 
                    "o2_reading": row[7], 
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
                    "set_point_o2": row[6],
                    "set_point_co2": row[8],
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
                #print(objetoV)
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

        #fecha ok 
        fecha_actual_ok = datetime.now()
        fecha_formateada = fecha_actual_ok.strftime("%Y-%m-%dT%H:%M:%S")
        #actualizar datos 
        actualizar_control = await collectionStarControl.update_one({"control": 1},{"$set":{"ij": ij+10,"fecha_t":fecha_formateada}})


    return imeis


async def homologar_starcool_general() -> dict:
    datazo = BaseConexion.obtener_mes_y_anio_actual()
    baseD = "REPOSITORIO_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    cnx = mysql.connector.connect(
        host= "localhost",
        user= "ztrack2023",
        passwd= "lpmp2018",
        database="zgroupztrack"
    )
    curConte = cnx.cursor(buffered=True)
    #contenedores starcool
    contenedores = ["ZGRU6844452","ZGRU6077903","ZGRU2010207","ZGRU1940045","ZGRU0029504","ZGRU6860448","ZGRU1092515","ZGRU1034969","ZGRU2008200","ZGRU8735478","ZGRU6859895","ZGRU9025691","ZGRU0084395","ZGRU1320227"]
    #recorrer lista 
    #for contenedor in contenedores:
    for index_1, contenedor in enumerate(contenedores):
        #print(contenedor)
        #buscar telemetrias de los equipos por base de datos en tabla contenedores
        consulta_contenedor = ("SELECT * FROM contenedores WHERE nombre_contenedor=%s")
        query_contenedor = curConte.execute(consulta_contenedor,(contenedor,))
        datos_contenedor = curConte.fetchall()
        datos_contenedor_acumulados =[]
        for row in datos_contenedor :
            datos_contenedor_acumulados.append(row)
            #print(row)
        if len(datos_contenedor_acumulados)>0:
            #significa que existe datos de la busqueda
            print(datos_contenedor_acumulados[0]) 
            print(str(datos_contenedor_acumulados[0][0]) + " , descripcion : "+ str(datos_contenedor_acumulados[0][4])+ " ,telemetria :"+ str(datos_contenedor_acumulados[0][9])) 
            print("aqui va el codigo : " + str(datos_contenedor_acumulados[0][1]))
            controlTelemetria = await collectionControl.find_one({"telemetria_id":datos_contenedor_acumulados[0][9]})
            idProgre = 20000000000+1000000000*(int(index_1))
            factorBusqueda ={}
            estadoC=0
            #print(controlTelemetria)
            if controlTelemetria :
                idProgre = controlTelemetria["id"]
                fechaId = controlTelemetria["fecha"]
                factorBusqueda ={"fecha":{"$gt":fechaId}}
                estadoC=1
            else : 
                datazo_anterior = obtener_mes_ano_anterior()
                baseD_anterior = "REPOSITORIO_"+datazo_anterior
                databaseMongo_anterior = client[baseD_anterior]
                collectionControl_anterior =databaseMongo_anterior.get_collection("control")
                controlTelemetria_anterior = await collectionControl_anterior.find_one({"telemetria_id":datos_contenedor_acumulados[0][9]})
                if controlTelemetria_anterior :
                    idProgre = controlTelemetria_anterior["id"]
                    fechaId = controlTelemetria_anterior["fecha"]
                    factorBusqueda ={"fecha":{"$gt":fechaId}}
                    estadoC=1
            print(estadoC)
            print(idProgre)
            collectionMongo = databaseMongo.get_collection("tunel")
            async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
                cad =x['data']
                fechaA=x['fecha']
                #SECTORIZAR LA TRAMA PARA UNIRLA 
                f2 =cad.split(',')
                #aqui empieza la homologazion
                if f2[2]==datos_contenedor_acumulados[0][1]:
                    #pasar por el algoritmo de procesamiento de informacion y homologar 
                    #1TC2,Madurador,ZGRU6844452,22,22,147,249,195,249,115,249,195,250,11,197,67,249,119,224,3,224,3,224,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0,0.00,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0,0,0.00,0.00,0.00,0.00,0.00,0,0,0,0.00,0.00,THERMOKING,0.000,0.000,0,0,0
                    if len(f2)>69 :
                        #cmd=[22,22,147,251,3,250,139,250,255,250,251,197,43,250,119,224,3,224,3,224]
                        datos_crudos = [f2[3],f2[4],f2[5],f2[6],f2[7],f2[8],f2[9],f2[10],f2[11],f2[12],f2[13],f2[14],f2[15]]
                        datos_homologados =transformar(datos_crudos)
                        #[sp,supply,ret,evap]
                        if len(datos_homologados)==4:
                            idProgre=idProgre+1

                            objetoV = {
                                "id": idProgre,
                                "set_point": datos_homologados[0], 
                                "temp_supply_1": datos_homologados[1],
                                "temp_supply_2": BaseConexion.convertir_a_float(f2[17]),
                                "return_air": datos_homologados[2], 
                                "evaporation_coil": datos_homologados[3],
                                "condensation_coil": BaseConexion.convertir_a_float(f2[18]),
                                "compress_coil_1": None,
                                "compress_coil_2": BaseConexion.convertir_a_float(f2[20]), 
                                "ambient_air": BaseConexion.convertir_a_float(f2[21]), 
                                "cargo_1_temp": BaseConexion.convertir_a_float(f2[22]),
                                "cargo_2_temp": BaseConexion.convertir_a_float(f2[23]), 
                                "cargo_3_temp": BaseConexion.convertir_a_float(f2[24]), 
                                "cargo_4_temp": BaseConexion.convertir_a_float(f2[25]), 
                                "relative_humidity": None, 
                                "avl": BaseConexion.convertir_a_float(f2[17]), 
                                "suction_pressure": BaseConexion.convertir_a_float(f2[18]), 
                                "discharge_pressure": BaseConexion.convertir_a_float(f2[19]), 
                                "line_voltage": BaseConexion.convertir_a_float(f2[20]), 
                                "line_frequency": BaseConexion.convertir_a_float(f2[21]), 
                                "consumption_ph_1": BaseConexion.convertir_a_float(f2[22]), 
                                "consumption_ph_2": BaseConexion.convertir_a_float(f2[23]), 
                                "consumption_ph_3": BaseConexion.convertir_a_float(f2[24]), 
                                "co2_reading": BaseConexion.convertir_a_float(f2[25]), 
                                "o2_reading": BaseConexion.convertir_a_float(f2[26]), 
                                "evaporator_speed": BaseConexion.convertir_a_float(f2[27]), 
                                "condenser_speed": BaseConexion.convertir_a_float(f2[28]),
                                "power_kwh": BaseConexion.convertir_a_float(f2[29]),
                                "power_trip_reading": BaseConexion.convertir_a_float(f2[30]),
                                "suction_temp": BaseConexion.convertir_a_float(f2[31]),
                                "discharge_temp": BaseConexion.convertir_a_float(f2[32]),
                                "supply_air_temp": BaseConexion.convertir_a_float(f2[33]),
                                "return_air_temp": BaseConexion.convertir_a_float(f2[34]),
                                "dl_battery_temp": BaseConexion.convertir_a_float(f2[35]),
                                "dl_battery_charge": BaseConexion.convertir_a_float(f2[36]),
                                "power_consumption": BaseConexion.convertir_a_float(f2[37]),
                                "power_consumption_avg": BaseConexion.convertir_a_float(f2[38]),
                                "alarm_present": BaseConexion.convertir_a_float(f2[39]),
                                "capacity_load": BaseConexion.convertir_a_float(f2[40]),
                                "power_state": 1, 
                                "controlling_mode": f2[42],
                                "humidity_control": BaseConexion.convertir_a_float(f2[43]),
                                "humidity_set_point": BaseConexion.convertir_a_float(f2[44]),
                                "fresh_air_ex_mode": BaseConexion.convertir_a_float(f2[45]),
                                "fresh_air_ex_rate": BaseConexion.convertir_a_float(f2[46]),
                                "fresh_air_ex_delay": BaseConexion.convertir_a_float(f2[47]),
                                "set_point_o2": BaseConexion.convertir_a_float(f2[48]),
                                "set_point_co2": BaseConexion.convertir_a_float(f2[49]),
                                "defrost_term_temp": BaseConexion.convertir_a_float(f2[50]),
                                "defrost_interval": BaseConexion.convertir_a_float(f2[51]),
                                "water_cooled_conde": BaseConexion.convertir_a_float(f2[52]),
                                "usda_trip": BaseConexion.convertir_a_float(f2[53]),
                                "evaporator_exp_valve": BaseConexion.convertir_a_float(f2[54]),
                                "suction_mod_valve": BaseConexion.convertir_a_float(f2[55]),
                                "hot_gas_valve": BaseConexion.convertir_a_float(f2[56]),
                                "economizer_valve": BaseConexion.convertir_a_float(f2[57]),
                                "ethylene": BaseConexion.convertir_a_float(f2[58]),
                                "stateProcess": f2[59],
                                "stateInyection": f2[60],
                                "timerOfProcess": BaseConexion.convertir_a_float(f2[61]),
                                "battery_voltage": BaseConexion.convertir_a_float(f2[62]),
                                "power_trip_duration":BaseConexion.convertir_a_float(f2[63]),
                                "modelo": f2[17],
                                "latitud": f2[17],
                                "longitud":  f2[17],
                                "created_at": fechaA,
                                "telemetria_id": datos_contenedor_acumulados[0][9],
                                "inyeccion_etileno": 0,
                                "defrost_prueba": 0,
                                "ripener_prueba": 0,
                                "sp_ethyleno": BaseConexion.convertir_a_float(f2[67]),
                                "inyeccion_hora": BaseConexion.convertir_a_float(f2[68]),
                                "inyeccion_pwm": BaseConexion.convertir_a_float(f2[69]),
                                "extra_1": 0,
                                "extra_2": 0,
                                "extra_3": 0,
                                "extra_4": 0,
                                "extra_5": 0
                            }
                            databaseMongoH = client['ztrack_ja']  
                            #collectionMongoH = databaseMongoH.get_collection("madurador_starcool")
                            collectionMongoH = databaseMongoH.get_collection("madurador")

                            collectionMongoH.insert_one(objetoV)
                            objetoControl ={
                                "id":idProgre,
                                "telemetria_id":objetoV['telemetria_id'],
                                "fecha":fechaA
                            }
                            if estadoC==1 :
                                #actualizar
                                collectionControl.update_one({"telemetria_id":objetoV['telemetria_id'],},{"$set": {"id":idProgre,"fecha":fechaA}})
                            else :
                                #grabar
                                collectionControl.insert_one(objetoControl)
                                estadoC=1
                            
                            curB = cnx.cursor()
                            update_old_salary = (
                            "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                            ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                                " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                            curB.execute(update_old_salary, (fechaA, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                                objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                                objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                                objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                                objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                                objetoV['telemetria_id'],  ))
                            cnx.commit()
        else :
            print("sin resultado")
    cnx.close()


async def homologar_starcool01() -> dict:
    #obtener el id de la telemetria en consulta MYSQL
    #STARCOOL01 es asignado a ZGRU1092515 con telemetria_id 14859 Y id_contenedor 474 , idProgre =16000000000
    datazo = BaseConexion.obtener_mes_y_anio_actual()
    #datazo ="7_2024"
    baseD = "REPOSITORIO_"+datazo
    databaseMongo = client[baseD]
    collectionControl =databaseMongo.get_collection("control")
    telemetry=14859
    controlTelemetria = await collectionControl.find_one({"telemetria_id":telemetry})
    idProgre = 16000004500
    factorBusqueda ={}
    estadoC=0
    #print(controlTelemetria)
    if controlTelemetria :
        idProgre = controlTelemetria["id"]
        fechaId = controlTelemetria["fecha"]
        factorBusqueda ={"fecha":{"$gt":fechaId}}
        estadoC=1
    trama=''
    collectionMongo = databaseMongo.get_collection("tunel")

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
    dataContenedor = curA.execute("SELECT * FROM contenedores WHERE nombre_contenedor='ZGRU1092515'")
    rows = curA.fetchall()
    conMysql =[]
    for row in rows :
        conMysql.append(row)
        print(row)
    #curA.close()
    async for x in collectionMongo.find(factorBusqueda).sort("fecha",1):
        cad =x['data']
        fechaA=x['fecha']
        #SECTORIZAR LA TRAMA PARA UNIRLA 
        f2 =cad.split(',')
        #aqui va la cadena la homolacion de datos de STARCOOL
        #



        if f2[2]=='STARCOOL01':
            if len(f2)==70:
                idProgre=idProgre+1
                #procesar el dato
                objetoV = {
                    "id": idProgre,
                    "set_point": BaseConexion.convertir_a_float(f2[14]), 
                    "temp_supply_1": BaseConexion.convertir_a_float(f2[15]),
                    "temp_supply_2": BaseConexion.convertir_a_float(f2[17]),
                    "return_air": BaseConexion.convertir_a_float(f2[16]), 
                    "evaporation_coil": BaseConexion.convertir_a_float(f2[17]),
                    "condensation_coil": BaseConexion.convertir_a_float(f2[18]),
                    "compress_coil_1": None,
                    "compress_coil_2": BaseConexion.convertir_a_float(f2[20]), 
                    "ambient_air": BaseConexion.convertir_a_float(f2[21]), 
                    "cargo_1_temp": BaseConexion.convertir_a_float(f2[22]),
                    "cargo_2_temp": BaseConexion.convertir_a_float(f2[23]), 
                    "cargo_3_temp": BaseConexion.convertir_a_float(f2[24]), 
                    "cargo_4_temp": BaseConexion.convertir_a_float(f2[25]), 
                    "relative_humidity": None, 
                    "avl": BaseConexion.convertir_a_float(f2[17]), 
                    "suction_pressure": BaseConexion.convertir_a_float(f2[18]), 
                    "discharge_pressure": BaseConexion.convertir_a_float(f2[19]), 
                    "line_voltage": BaseConexion.convertir_a_float(f2[20]), 
                    "line_frequency": BaseConexion.convertir_a_float(f2[21]), 
                    "consumption_ph_1": BaseConexion.convertir_a_float(f2[22]), 
                    "consumption_ph_2": BaseConexion.convertir_a_float(f2[23]), 
                    "consumption_ph_3": BaseConexion.convertir_a_float(f2[24]), 
                    "co2_reading": BaseConexion.convertir_a_float(f2[25]), 
                    "o2_reading": BaseConexion.convertir_a_float(f2[26]), 
                    "evaporator_speed": BaseConexion.convertir_a_float(f2[27]), 
                    "condenser_speed": BaseConexion.convertir_a_float(f2[28]),
                    "power_kwh": BaseConexion.convertir_a_float(f2[29]),
                    "power_trip_reading": BaseConexion.convertir_a_float(f2[30]),
                    "suction_temp": BaseConexion.convertir_a_float(f2[31]),
                    "discharge_temp": BaseConexion.convertir_a_float(f2[32]),
                    "supply_air_temp": BaseConexion.convertir_a_float(f2[33]),
                    "return_air_temp": BaseConexion.convertir_a_float(f2[34]),
                    "dl_battery_temp": BaseConexion.convertir_a_float(f2[35]),
                    "dl_battery_charge": BaseConexion.convertir_a_float(f2[36]),
                    "power_consumption": BaseConexion.convertir_a_float(f2[37]),
                    "power_consumption_avg": BaseConexion.convertir_a_float(f2[38]),
                    "alarm_present": BaseConexion.convertir_a_float(f2[39]),
                    "capacity_load": BaseConexion.convertir_a_float(f2[40]),
                    "power_state": 1, 
                    "controlling_mode": f2[42],
                    "humidity_control": BaseConexion.convertir_a_float(f2[43]),
                    "humidity_set_point": BaseConexion.convertir_a_float(f2[44]),
                    "fresh_air_ex_mode": BaseConexion.convertir_a_float(f2[45]),
                    "fresh_air_ex_rate": BaseConexion.convertir_a_float(f2[46]),
                    "fresh_air_ex_delay": BaseConexion.convertir_a_float(f2[47]),
                    "set_point_o2": BaseConexion.convertir_a_float(f2[48]),
                    "set_point_co2": BaseConexion.convertir_a_float(f2[49]),
                    "defrost_term_temp": BaseConexion.convertir_a_float(f2[50]),
                    "defrost_interval": BaseConexion.convertir_a_float(f2[51]),
                    "water_cooled_conde": BaseConexion.convertir_a_float(f2[52]),
                    "usda_trip": BaseConexion.convertir_a_float(f2[53]),
                    "evaporator_exp_valve": BaseConexion.convertir_a_float(f2[54]),
                    "suction_mod_valve": BaseConexion.convertir_a_float(f2[55]),
                    "hot_gas_valve": BaseConexion.convertir_a_float(f2[56]),
                    "economizer_valve": BaseConexion.convertir_a_float(f2[57]),
                    "ethylene": BaseConexion.convertir_a_float(f2[58]),
                    "stateProcess": f2[59],
                    "stateInyection": f2[60],
                    "timerOfProcess": BaseConexion.convertir_a_float(f2[61]),
                    "battery_voltage": BaseConexion.convertir_a_float(f2[62]),
                    "power_trip_duration":BaseConexion.convertir_a_float(f2[63]),
                    "modelo": f2[17],
                    "latitud": f2[17],
                    "longitud":  f2[17],
                    "created_at": fechaA,
                    "telemetria_id": telemetry,
                    "inyeccion_etileno": 0,
                    "defrost_prueba": 0,
                    "ripener_prueba": 0,
                    "sp_ethyleno": BaseConexion.convertir_a_float(f2[67]),
                    "inyeccion_hora": BaseConexion.convertir_a_float(f2[68]),
                    "inyeccion_pwm": BaseConexion.convertir_a_float(f2[69]),
                    "extra_1": 0,
                    "extra_2": 0,
                    "extra_3": 0,
                    "extra_4": 0,
                    "extra_5": 0
                }

                databaseMongoH = client['ztrack_ja']  
                collectionMongoH = databaseMongoH.get_collection("madurador")
                collectionMongoH.insert_one(objetoV)
                objetoControl ={
                    "id":idProgre,
                    "telemetria_id":telemetry,
                    "fecha":fechaA
                }
                if estadoC==1 :
                    #actualizar
                    collectionControl.update_one({"telemetria_id":telemetry,},{"$set": {"id":idProgre,"fecha":fechaA}})
                else :
                    #grabar
                    collectionControl.insert_one(objetoControl)
                    estadoC=1
                
                curB = cnx.cursor()
                update_old_salary = (
                "UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
                ", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
                    " , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s WHERE estado = 1 AND telemetria_id = %s  ")
                curB.execute(update_old_salary, (fechaA, objetoV['set_point'],objetoV['temp_supply_1'], 
                                                    objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                                    objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                                    objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                                    objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                                    objetoV['telemetria_id'],  ))
                cnx.commit()
    cnx.close()            
                    

# ============================================================================
# CONFIGURACIÓN MYSQL CON POOL
# ============================================================================

mysql_config = {
    "pool_name": "starcool_pool",
    "pool_size": 15,
    "pool_reset_session": True,
    "host": "localhost",
    "user": "ztrack2023",
    "passwd": "lpmp2018",
    "database": "zgroupztrack",
    "autocommit": False,
    "connect_timeout": 10,
    "use_pure": False
}

try:
    mysql_pool = mysql.connector.pooling.MySQLConnectionPool(**mysql_config)
except mysql.connector.Error as err:
    print(f"Error creando pool MySQL: {err}")
    mysql_pool = None

# Semáforo para limitar concurrencia
mysql_semaphore = asyncio.Semaphore(10)

@asynccontextmanager
async def get_mysql_connection(timeout: int = 30):
    """Context manager seguro para conexiones MySQL"""
    cnx = None
    cursor = None
    retry_count = 0
    max_retries = 3
    
    async with mysql_semaphore:
        while retry_count < max_retries:
            try:
                cnx = mysql_pool.get_connection()
                
                # Configurar timeouts
                cursor = cnx.cursor()
                cursor.execute("SET SESSION innodb_lock_wait_timeout = 10")
                cursor.execute("SET SESSION lock_wait_timeout = 10")
                cursor.close()
                
                yield cnx
                
                if cnx.in_transaction:
                    cnx.commit()
                break
                
            except mysql.connector.errors.DatabaseError as e:
                retry_count += 1
                print(f"Error MySQL (intento {retry_count}/{max_retries}): {e}")
                
                if cnx:
                    try:
                        cnx.rollback()
                    except:
                        pass
                
                if "Lock wait timeout" in str(e) or "Deadlock" in str(e):
                    if retry_count < max_retries:
                        await asyncio.sleep(0.5 * retry_count)
                        continue
                raise
                
            except Exception as e:
                print(f"Error inesperado en MySQL: {e}")
                if cnx:
                    try:
                        cnx.rollback()
                    except:
                        pass
                raise
                
            finally:
                if cnx and retry_count >= max_retries:
                    try:
                        cnx.close()
                    except:
                        pass

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def extraer_datos_starcool(notificacion: dict) -> Optional[str]:
    """
    Intenta extraer datos de d01, si falla prueba con d02
    Retorna la cadena de datos o None si no encuentra nada válido
    """
    # Primero intentar con d01
    if 'd01' in notificacion and notificacion['d01']:
        captura_datos = notificacion['d01']
        if len(captura_datos) > 100:
            print(f"✓ Datos encontrados en d01: {len(captura_datos)} caracteres")
            return captura_datos
        else:
            print(f"✗ d01 insuficiente: {len(captura_datos)} caracteres")
    
    # Si d01 falla, intentar con d02
    if 'd02' in notificacion and notificacion['d02']:
        captura_datos = notificacion['d02']
        if len(captura_datos) > 100:
            print(f"✓ Datos encontrados en d02: {len(captura_datos)} caracteres")
            return captura_datos
        else:
            print(f"✗ d02 insuficiente: {len(captura_datos)} caracteres")
    
    print("✗ No se encontraron datos válidos en d01 ni d02")
    return None

async def obtener_o_crear_telemetria(cursor, imei: str) -> int:
    """
    Obtiene ID de telemetría existente o crea uno nuevo
    """
    identi = f"S{imei}"
    
    # Buscar telemetría existente
    consulta_telemetria = "SELECT id FROM telemetrias WHERE imei=%s AND estado=1"
    cursor.execute(consulta_telemetria, (identi,))
    resultado = cursor.fetchone()
    
    if resultado:
        return resultado[0]
    
    # No existe, obtener último ID
    consulta_ultimo_id = "SELECT id FROM telemetrias ORDER BY id DESC LIMIT 1"
    cursor.execute(consulta_ultimo_id)
    ultimo = cursor.fetchone()
    
    nuevo_id = (ultimo[0] + 1) if ultimo else 1
    
    # Crear nueva telemetría
    insert_telemetria = (
        "INSERT INTO telemetrias (id, numero_telefono, imei, estado) "
        "VALUES (%s, %s, %s, 1)"
    )
    cursor.execute(insert_telemetria, (nuevo_id, identi, identi))
    
    return nuevo_id

async def obtener_o_crear_contenedor(cursor, telemetria_id: int, imei: str) -> bool:
    """
    Verifica si existe contenedor, si no lo crea
    Retorna True si se creó, False si ya existía
    """
    identi = f"S{imei}"
    
    # Buscar contenedor existente
    consulta_contenedor = "SELECT id FROM contenedores WHERE telemetria_id=%s AND estado=1"
    cursor.execute(consulta_contenedor, (telemetria_id,))
    resultado = cursor.fetchone()
    
    if resultado:
        return False  # Ya existe
    
    # Crear nuevo contenedor
    insert_contenedor = (
        "INSERT INTO contenedores (nombre_contenedor, tipo, telemetria_id, estado) "
        "VALUES (%s, %s, %s, 1)"
    )
    cursor.execute(insert_contenedor, (identi, "Madurador", telemetria_id))
    
    return True  # Creado

def construir_objeto_starcool(row: List, ij: int, fecha: datetime, telemetria_id: int) -> dict:
    """
    Construye objeto de telemetría para StarCool
    """
    return {
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
        "co2_reading": row[9], 
        "o2_reading": row[7], 
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
        "set_point_o2": row[6],
        "set_point_co2": row[8],
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
        "power_trip_duration": 0.00,
        "modelo": "STARCOOL",
        "latitud": 0.00,
        "longitud": 0.00,
        "created_at": fecha,
        "telemetria_id": telemetria_id,
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

# ============================================================================
# PROCESAMIENTO POR LOTES CON MANEJO ROBUSTO
# ============================================================================

async def procesar_batch_starcool(
    batch_objetos: List[dict],
    collection_mongo,
    batch_size: int = 20
):
    """
    Procesa lote de objetos en MongoDB y MySQL
    """
    if not batch_objetos:
        return
    
    # 1. Insertar en MongoDB (más confiable)
    try:
        await collection_mongo.insert_many(batch_objetos, ordered=False)
    except Exception as e:
        print(f"Error batch MongoDB: {e}")
        # Insertar uno por uno
        for obj in batch_objetos:
            try:
                await collection_mongo.insert_one(obj)
            except Exception as e2:
                print(f"Error individual MongoDB: {e2}")
    
    # 2. Actualizar MySQL en sub-lotes pequeños
    for i in range(0, len(batch_objetos), batch_size):
        mini_batch = batch_objetos[i:i + batch_size]
        await actualizar_mysql_batch(mini_batch)
        await asyncio.sleep(0.01)  # Pausa entre batches

async def actualizar_mysql_batch(objetos: List[dict]):
    """
    Actualiza MySQL con retry logic
    """
    update_query = """
        UPDATE contenedores 
        SET ultima_fecha = %s, set_point = %s, temp_supply_1 = %s, 
            return_air = %s, ambient_air = %s, relative_humidity = %s, 
            avl = %s, defrost_prueba = %s, ripener_prueba = %s, 
            ethylene = %s, set_point_co2 = %s, co2_reading = %s, 
            humidity_set_point = %s, sp_ethyleno = %s, compress_coil_1 = %s 
        WHERE estado = 1 AND telemetria_id = %s
    """
    
    try:
        async with get_mysql_connection() as cnx:
            cursor = cnx.cursor()
            
            # Preparar datos
            mysql_data = [
                (
                    obj['created_at'], obj['set_point'], obj['temp_supply_1'],
                    obj['return_air'], obj['ambient_air'], obj['relative_humidity'],
                    obj['avl'], obj['inyeccion_pwm'], obj['inyeccion_hora'],
                    obj['ethylene'], obj['set_point_co2'], obj['co2_reading'],
                    obj['humidity_set_point'], obj['sp_ethyleno'], obj['compress_coil_1'],
                    obj['telemetria_id']
                )
                for obj in objetos
            ]
            
            cursor.executemany(update_query, mysql_data)
            cnx.commit()
            cursor.close()
            
    except mysql.connector.errors.DatabaseError as e:
        print(f"Error MySQL batch: {e}")
        # Procesar individualmente
        await actualizar_mysql_individual(objetos)
    except Exception as e:
        print(f"Error inesperado MySQL: {e}")

async def actualizar_mysql_individual(objetos: List[dict]):
    """
    Actualiza MySQL uno por uno en caso de fallo del batch
    """
    update_query = """
        UPDATE contenedores 
        SET ultima_fecha = %s, set_point = %s, temp_supply_1 = %s, 
            return_air = %s, ambient_air = %s, relative_humidity = %s, 
            avl = %s, defrost_prueba = %s, ripener_prueba = %s, 
            ethylene = %s, set_point_co2 = %s, co2_reading = %s, 
            humidity_set_point = %s, sp_ethyleno = %s, compress_coil_1 = %s 
        WHERE estado = 1 AND telemetria_id = %s
    """
    
    for obj in objetos:
        retry_count = 0
        max_retries = 2
        
        while retry_count < max_retries:
            try:
                async with get_mysql_connection() as cnx:
                    cursor = cnx.cursor()
                    
                    data = (
                        obj['created_at'], obj['set_point'], obj['temp_supply_1'],
                        obj['return_air'], obj['ambient_air'], obj['relative_humidity'],
                        obj['avl'], obj['inyeccion_pwm'], obj['inyeccion_hora'],
                        obj['ethylene'], obj['set_point_co2'], obj['co2_reading'],
                        obj['humidity_set_point'], obj['sp_ethyleno'], obj['compress_coil_1'],
                        obj['telemetria_id']
                    )
                    
                    cursor.execute(update_query, data)
                    cnx.commit()
                    cursor.close()
                    break
                    
            except mysql.connector.errors.DatabaseError as e:
                retry_count += 1
                print(f"Error individual MySQL (intento {retry_count}): {e}")
                if retry_count < max_retries:
                    await asyncio.sleep(0.2 * retry_count)
                else:
                    print(f"Fallo definitivo para telemetria_id {obj['telemetria_id']}")
            except Exception as e:
                print(f"Error inesperado: {e}")
                break

# ============================================================================
# FUNCIÓN PRINCIPAL OPTIMIZADA
# ============================================================================

async def procesar_starcool_optimizado():
    """
    Procesa dispositivos StarCool con manejo robusto de errores
    """
    imeis = []
    
    # Colecciones MongoDB
    collectionImei = databaseMongo.get_collection("dispositivos_starcool")
    collectionStarControl = databaseMongo.get_collection("control_starcool")
    
    # Obtener control
    controlStarCool = await collectionStarControl.find_one({"control": 1}, {"_id": 0})
    if not controlStarCool:
        print("No se encontró registro de control")
        return []
    
    ij_inicial = controlStarCool.get('ij', 241000)
    fecha_t = controlStarCool.get('fecha_t', '2024-12-11T23:35:54')
    fecha_ok = datetime.fromisoformat(fecha_t)
    
    # MongoDB destino
    databaseMongoH = client['ztrack_ja']
    collectionMongoH = databaseMongoH.get_collection("madurador")
    
    # Procesar cada IMEI
    async for x in collectionImei.find():
        imei = x['imei']
        imeis.append(imei)
        
        print("=" * 50)
        print(f"Procesando IMEI: {imei}")
        print("=" * 50)
        
        try:
            # Usar connection pool para MySQL
            async with get_mysql_connection() as cnx:
                cursor = cnx.cursor()
                
                # Obtener o crear telemetría
                id_obtenido = await obtener_o_crear_telemetria(cursor, imei)
                print(f"Telemetria ID: {id_obtenido}")
                
                # Obtener o crear contenedor
                contenedor_creado = await obtener_o_crear_contenedor(cursor, id_obtenido, imei)
                if contenedor_creado:
                    print(f"✓ Contenedor creado para {imei}")
                
                cnx.commit()
                
        except Exception as e:
            print(f"Error configurando dispositivo {imei}: {e}")
            continue
        
        # Procesar datos históricos
        base_imei = obtener_mes_ano_anterior_imei(str(imei))
        collection_especifica = databaseMongo.get_collection(base_imei)
        
        factorBusqueda = {"fecha": {"$gt": fecha_ok}}
        
        # Batch para procesar
        batch_objetos = []
        ij = ij_inicial
        contador_procesados = 0
        contador_fallidos = 0
        
        cursor_mongo = collection_especifica.find(
            factorBusqueda, 
            {"_id": 0}
        ).sort("fecha", 1)
        
        async for notificacion in cursor_mongo:
            try:
                # Intentar extraer datos de d01, si falla usar d02
                captura_datos = extraer_datos_starcool(notificacion)
                
                if not captura_datos:
                    contador_fallidos += 1
                    continue
                
                # Procesar datos
                row = resultados_starcool(captura_datos[6:])
                
                # Construir objeto
                objetoV = construir_objeto_starcool(
                    row, 
                    ij, 
                    notificacion['fecha'], 
                    id_obtenido
                )
                
                batch_objetos.append(objetoV)
                ij += 1
                contador_procesados += 1
                
                # Procesar batch cada 50 registros
                if len(batch_objetos) >= 50:
                    await procesar_batch_starcool(batch_objetos, collectionMongoH)
                    batch_objetos = []
                    print(f"✓ Procesados: {contador_procesados}, Fallidos: {contador_fallidos}")
                
            except Exception as e:
                print(f"Error procesando notificación: {e}")
                contador_fallidos += 1
                continue
        
        # Procesar batch restante
        if batch_objetos:
            await procesar_batch_starcool(batch_objetos, collectionMongoH)
        
        # Actualizar contador
        ij_inicial = ij + 10
        
        print(f"\n{'='*50}")
        print(f"IMEI {imei} completado:")
        print(f"  ✓ Procesados: {contador_procesados}")
        print(f"  ✗ Fallidos: {contador_fallidos}")
        print(f"{'='*50}\n")
    
    # Actualizar control final
    try:
        fecha_actual_ok = datetime.now()
        fecha_formateada = fecha_actual_ok.strftime("%Y-%m-%dT%H:%M:%S")
        
        await collectionStarControl.update_one(
            {"control": 1},
            {"$set": {"ij": ij_inicial, "fecha_t": fecha_formateada}}
        )
        print(f"✓ Control actualizado: ij={ij_inicial}, fecha={fecha_formateada}")
    except Exception as e:
        print(f"Error actualizando control: {e}")
    
    return imeis
