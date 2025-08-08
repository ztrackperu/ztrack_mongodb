import json
from datetime import datetime
res = []
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
ij =10000
id_obtenido = 15253
# Leer el archivo JSON
with open("atmos.json", "r") as file:
    data = json.load(file)

# Procesar cada registro y agregar los nuevos campos

for record in data:

    trama_original = record.get("d01", "")
    if len(trama_original) >= 80:  # Verificamos que haya suficientes caracteres
        #print("bueno")
        row = resultados_starcool(trama_original[6:])
        #print(row)
        #['Set Point', 'Supply 1 temp', 'Return temp', 'Evaporator temp', 'Ambient temp', 'Supply 2 temp']
            # return [set_point,supply_1,retorno,evap,ambien,supply_2 ,o2_set,o2_reading,co2_set,co2_reading]
        ij += 1
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
            "created_at": record['fecha'],
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
        
        res.append(objetoV)


 


# Guardar los datos modificados de nuevo en el archivo JSON
#with open('atmosfera_ok.json', 'w') as file:
    #json.dump(data, file, indent=4)
print(res[100])
print("Campos 'create_at' y 'telemetria_id' añadidos correctamente.")

with open("resultado.json", "w") as f:
    json.dump(res, f, indent=4)


