from datetime import datetime, timedelta

def procesar_12_horas(ultimo):
    fechaF = datetime.fromisoformat(ultimo)
    hora12 = timedelta(hours=12)
    hora11 = timedelta(hours=11)
    fechaI = fechaF-hora12
    fecha2 = fechaF-hora11
    data = [fechaI,fecha2,fechaF]
    return data

def obtener_meses_en_rango(fecha_inicio, fecha_fin):
    # Convertir las fechas de string a objetos datetime
    inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
    fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
    
    # Lista para almacenar los meses
    meses = []

    # Iterar sobre los meses en el rango
    while inicio <= fin:
        # Agregar el mes actual a la lista
        meses.append(inicio.strftime('%m_%Y'))
        # Avanzar al siguiente mes
        inicio += timedelta(days=32)
        inicio = inicio.replace(day=1)

    return meses


datosDepurar = [
    32752,-32752, 3275.2, -3275.2, 327.52,-327.52, 32767, -32767, 3276.7, -3276.7, 327.67, -327.67,32766, -32766 , 3276.6, -3276.6, 327.66, -327.66,
    32765, -32765, 3276.5, -3276.5, 327.65, -327.65,32764, -32764, 3276.4, -3276.4, 327.64, -327.64,32763, -32763, 3276.3, -3276.3, 327.63, -327.63,
    32762, -32762, 3276.2, -3276.2, 327.62, -327.62, 32761, -32761, 3276.1, -3276.1, 327.61, -327.61,32760, -32760, 3276.0, -3276.0, 327.60, -327.60,
    32759, -32759, 3275.9, -3275.9, 327.59, -327.59,32751, -32751, 3275.1, -3275.1, 327.51, -327.51,-3277,-3276.9,-38.5,25.4,255,18559,65151
]
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