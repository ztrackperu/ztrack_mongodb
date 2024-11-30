import csv
import json
import mysql.connector
from server.database import client
from bson import regex
from datetime import datetime,timedelta
from server.generico.base_conexion import BaseConexion
from dateutil.relativedelta import relativedelta
import os

db_connection = mysql.connector.connect(
    host= "localhost",
    user= "ztrack2023",
    passwd= "lpmp2018",
    database="zgroupztrack"
)


def obtener_mes_ano_anterior():
    # Obtener la fecha actual
    fecha_actual = datetime.now()
    # Restar un mes
    fecha_anterior = fecha_actual - relativedelta(months=1)
    # Formatear mes y año anterior en el formato deseado
    repositorio = f"REPOSITORIO_{fecha_anterior.strftime('%m')}_{fecha_anterior.strftime('%Y')}"
    return repositorio


def Calcula_Termino1(valve):
#FUNCION CALCULA SP    
    aux = valve
    signo = 0
    aux = aux & 0xF000
    if(aux == 0xF000):
        signo = 1
        valve = valve - 0xF000
    else:
        valve = valve - 0xC000
    valve = valve >> 4
    if(signo==1):
        valve = 0x100 - valve
    valve = valve / 4.0
    if(signo == 1):
        valve = -valve
    return valve

#VALOR DE SETPOINT

def pasar_dato(com1 ,com2):
    val = 0xFF
    val = val & int(com1)
    val = val << 8
    val = val & 0xFFFF
    val = val | int(com2)
    sp = Calcula_Termino1(val)
    return sp

def transformar(arr):
    res = []
    enum = "Valor SP: "
    sp = pasar_dato(arr[3] ,arr[4])
    #print(sp)
    #res.append(enum)
    res.append(sp)

    enum = "Valor SUply: "
    sp = pasar_dato(arr[5] ,arr[6])
    #print(sp)
    #res.append(enum)
    res.append(sp)

    enum = "Valor retur: "
    sp = pasar_dato(arr[7] ,arr[8])
    #print(sp)
    #res.append(enum)
    res.append(sp)

    enum = "Valor evap: "
    sp = pasar_dato(arr[9] ,arr[10])
    #print(sp)
    #res.append(enum)
    res.append(sp)

    return res


async def homologar_simular_ransa() ->dict :
    csv_file = os.path.join(os.path.dirname(__file__), 'data', 'ZGRU4729220.csv')
    #csv_file = 'ZGRU4729220.csv' 
    json_file = 'resultado.json'
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        # Lista para almacenar los diccionarios
        data = []
        # Recorrer cada línea del CSV
        for row in reader:
            # Crear el diccionario con los valores de la fila
            entry = {
                'nombre': row[0],       # 'ZGRU2018234'
                'set': row[1],          # '-25.00'
                'supply': row[2],       # '-29.00'
                'return': row[3],       # '-24.60'
                'evap': row[4],         # '-27.00'
                'coil': row[5]          # '23.30'
            }
            # Añadir el diccionario a la lista de datos
            data.append(entry)

    # Guardar los datos en un archivo JSON
    with open(json_file, 'w') as json_out:
        json.dump(data, json_out, indent=4)
    print(f"Archivo JSON generado en {json_file}")



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


    csv_file = 'ZGRU4729220.csv'
    json_file = 'resultado.json'






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
                    






