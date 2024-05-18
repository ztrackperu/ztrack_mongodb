import json
from app.server.database1 import collection
from bson import regex

def notificacion_helper(notificacion) -> dict: 
    return {
        "numNotificacion": notificacion["numNotificacion"],
        "asunto": notificacion["asunto"],
        "numOT":notificacion.get("numOT",None),
        "numSolicitud":  notificacion.get("numSolicitud",None),
        "fechaN": notificacion["fechaN"],
        "trabajo": notificacion["trabajo"],
        "perfil": notificacion["perfil"],
        "estadoN": notificacion["estadoN"],
    } 
notificacion_collection = collection("notificaciones")
# crud operation
# Recuperar todos los notificacions presentes en la base de datos.
async def retrieve_notificacions():
    notificacions = []
    async for notificacion in notificacion_collection.find({"estadoN":1}):
        #print(notificacion)
        notificacions.append(notificacion_helper(notificacion))
    return notificacions


# Agregar un nuevo notificacion a la base de datos
async def add_notificacion(notificacion_data: dict) -> dict:
    #aqui envia el json a mongo y lo inserta
    notificacion = await notificacion_collection.insert_one(notificacion_data)
    #aqui busca el dato obtenido para mostrarlo como respuesta
    new_notificacion = await notificacion_collection.find_one({"_id": notificacion.inserted_id})
    return notificacion_helper(new_notificacion)

# Recuperar un notificacion con un ID coincidente
async def retrieve_notificacion(id: int) -> dict:
    #print(id)
    #importante convertir a int cunado se busca a un dato por numero
    notificacion = await notificacion_collection.find_one({"numNotificacion": int(id)})
    #print(notificacion)
    if notificacion:
        return notificacion_helper(notificacion) 

# Actualizar a un estudiante con un ID coincidente
async def update_notificacion(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    
    notificacion = await notificacion_collection.find_one({"numNotificacion": id})
    if notificacion:
        updated_notificacion = await notificacion_collection.update_one(
            {"numNotificacion": id}, {"$set": data}
        )
        if updated_notificacion:
            return True
        return False

# Eliminar un notificacion de la base de datos
async def delete_notificacion(id: int):
    notificacion = await notificacion_collection.find_one({"numNotificacion": id})
    if notificacion:
        await notificacion_collection.delete_one({"numNotificacion": id})
        return True
    
# Extraer el ultimo  notificacion de la base de datos en base al campo id
async def extraer_notificacion()->dict:
    notificacions = []
    async for notificacion in notificacion_collection.find({"estadoN":1},{"_id":0,"numNotificacion":1}).sort({"numNotificacion":-1}).limit(1):
        print(notificacion)
        notificacions.append(notificacion)
    #se debe extraer el primir resultado
    return notificacions[0]

