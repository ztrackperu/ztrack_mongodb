trama = "161693C503E003C47BE003E003E003E003E003E003E003004178009D0000190711001E0CFE324F280903FFFFFFFFFFFFFFFFFFFFFFFFD9A7D786D7DED47ED46CD469D4CBD4CFD6D0D07B0000000000000000000000000000000000000000040000000000D6A9"

# Paso 1: Eliminar los primeros 6 caracteres
trama_recortada = trama[6:]

# Paso 2: Obtener el par de caracteres en posición 70 (índice 70 y 71)
# Recuerda que los índices en Python son base 0
hex_par_0 = trama_recortada[68:70]
hex_par = trama_recortada[70:72]

hex_par_1 = trama_recortada[72:74]
hex_par_2 = trama_recortada[74:76]
hex_par_3 = trama_recortada[76:78]
# Paso 3: Convertir de hexadecimal a decimal
valor_decimal_0 = int(hex_par_0, 16)


valor_decimal = int(hex_par, 16)

valor_decimal_1 = int(hex_par_1, 16)
valor_decimal_2 = int(hex_par_2, 16)
valor_decimal_3 = int(hex_par_3, 16)

# Paso 4: Dividir entre 10
#resultado = valor_decimal / 10
resultado_0 = valor_decimal_0 / 10

resultado = valor_decimal / 10
resultado_1 = valor_decimal_1 / 10
resultado_2 = valor_decimal_2 / 10
resultado_3 = valor_decimal_3 / 10


# Mostrar resultados
print("Trama recortada:", trama_recortada)
print("Par hex en posición 68-69:", hex_par_0)
print("Valor decimal:", valor_decimal_0)
print("Resultado final (decimal / 10):", resultado_0)



print("Par hex en posición 70-71:", hex_par)
print("Valor decimal:", valor_decimal)
print("Resultado final (decimal / 10):", resultado)

print("Par hex en posición 72-73:", hex_par_1)
print("Valor decimal:", valor_decimal_1)
print("Resultado final (decimal / 10):", resultado_1)

print("Par hex en posición 74-75:", hex_par_2)
print("Valor decimal:", valor_decimal_2)
print("Resultado final (decimal / 10):", resultado_2)

print("Par hex en posición 75-76:", hex_par_3)
print("Valor decimal:", valor_decimal_3)
print("Resultado final (decimal / 10):", resultado_3)

    #opciones de datos o2 setpoint , o2 , co2 setpoint , co2  : 35,36,37,38


def Get_Number_starcool_one(vector,index,Bytes):
    inicio = int(index*Bytes)
    fin = int((index+1)*Bytes)
    trama_recortada = vector[inicio:fin]
    valor_decimal = int(trama_recortada, 16)
    resultado = valor_decimal / 10
    return resultado


set_o2 = Get_Number_starcool_one(trama_recortada, 34, 2)
print("O2 Setpoint:", set_o2)
o2_reading = Get_Number_starcool_one(trama_recortada, 35, 2)
print("O2 Reading:", o2_reading)
set_point_co2 = Get_Number_starcool_one(trama_recortada, 36, 2)
print("CO2 Setpoint:", set_point_co2)
co2_reading = Get_Number_starcool_one(trama_recortada, 37, 2)
print("CO2 Reading:", co2_reading)  



