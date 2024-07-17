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
        if proceso==0:
            fecha_anterior=x['fecha']
            print('insertar')
            proceso=1
        else:
            #dato proceso de fecha
            if (x['fecha']-fecha_anterior)>30 :
                print('insertar')
            proceso=0
            
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
