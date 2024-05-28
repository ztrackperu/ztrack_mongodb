from datetime import datetime, timedelta

def agregar_datos_por_intervalo(json_data, interval_minutes=10):
    # Extraer los datos del JSON
    data = json_data["graph"]
    created_at = data["created_at"]["data"]
    return_air = data["return_air"]["data"]
    
    # Convertir las fechas a objetos datetime
    created_at = [datetime.fromisoformat(date_str) for date_str in created_at]
    
    # Inicializar variables para el bucle
    current_time = created_at[0]
    current_interval_end = current_time + timedelta(minutes=interval_minutes)
    current_array = []
    final_data = []
    last_return_air = None
    
    # Iterar sobre los datos
    for time, ra in zip(created_at, return_air):
        # Si estamos dentro del intervalo actual
        if time < current_interval_end:
            # Si es el primer elemento o la variación de return_air es superior o inferior al 5%
            if last_return_air is None or abs((ra - last_return_air) / last_return_air) * 100 > 5:
                current_array.append({"time": time.isoformat(), "return_air": ra})
            last_return_air = ra
        else:
            # Agregar el array actual al resultado final
            final_data.append(current_array)
            # Iniciar un nuevo array para el nuevo intervalo
            current_array = [{"time": time.isoformat(), "return_air": ra}]
            # Actualizar el tiempo del nuevo intervalo
            current_time = time
            current_interval_end = current_time + timedelta(minutes=interval_minutes)
            last_return_air = ra
    
    # Agregar el último intervalo al resultado final
    final_data.append(current_array)
    
    return final_data




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
    for i in range(len(graph)):
        nombre_lista = f"{graph[i]['label']}"
        cadena.append(graph[i]['label'])
        lab = procesar_texto(graph[i]['label'])
        listas[nombre_lista] = {
            "data":[],
            "config":[lab,graph[i]['hidden'],graph[i]['color'],graph[i]['tipo']]
        }
    #print(bconsultas)


    

    if(len(bconsultas)==1):
        database = client[bconsultas[0]]
        madurador = database.get_collection("madurador")
        pip = [
            {"$match": {"$and":[{"created_at": {"$gte": fech[0]}},{"created_at": {"$lte": fech[1]}}]}},  
            {"$project":dataConfig['config_data']},
            {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},
            {"$limit" : notificacion_data['size']},  
        ]
        minutosP =2
        delta =5
        concepto_ots = []
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
    else:
        for i in range(len(bconsultas)):
            print(i)
            if(i==0):
                diferencial =[{"created_at": {"$gte": fech[0]}}]
            else :
                if(i==len(bconsultas)-1):
                    diferencial =[{"created_at": {"$lte": fech[1]}}]    
                else:
                    diferencial=[]
            pip = [
                {"$match": {"$and":diferencial}},  
                {"$project":dataConfig['config_data']},
                {"$skip" : (notificacion_data['page']-1)*notificacion_data['size']},
                {"$limit" : notificacion_data['size']},  
            ]
            database = client[bconsultas[i]]
            madurador = database.get_collection("madurador")
            concepto_ots = []
            minutosP =2
            delta =8
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
    return listasT