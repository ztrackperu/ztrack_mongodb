from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
#from fastapi_pagination import Page, add_pagination
from fastapi_pagination import Page, add_pagination, paginate
#from fastapi_pagination.ext.motor import paginate

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.madurador import (
    data_madurador,
    obtener_madurador,
    data_tunel,
    data_wonderful,
    homologar_tunel_2,
    homologar_wonderful_zgru1090804,
    homologar_wonderful_zgru2009227,
    homologar_wonderful_zgru2008220,
    homologar_wonderful_zgru2232647,
    homologar_wonderful_zgru2009227_2,
    homologar_wonderful_zgru1090804_2,
    homologar_wonderful_zgru2008220_2,
    homologar_wonderful_zgru2232647_2,
    starcool_ZGRU1092515,
    data_madurador_filadelfia,
    homologar_datos_wonderful,
    data_madurador_tabla,
    data_pollito,
    data_ztrack_ja,
    tabla_ztrack_ja
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudMaduradorSchema,
    DatosMadurador,
    TunelSchema,
    ProcesarWonderfulSchema,
    WonderfulSchema,
    SolicitudMaduradorSchemaF,
    SolicitudZtrackSchema,

)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/TablaZtrack/", response_description="Datos de los notificacion agregados a la base de datos.")
async def tabla_ztrack_data(notificacion: SolicitudZtrackSchema = Body(...)):
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await tabla_ztrack_ja(notificacion)
    return ResponseModel(new_notificacion, "ok")


@router.post("/DatosZtrack/", response_description="Datos de los notificacion agregados a la base de datos.")
async def add_ztrack_data(notificacion: SolicitudZtrackSchema = Body(...)):
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_ztrack_ja(notificacion)
    return ResponseModel(new_notificacion, "ok")


@router.post("/DatosGraficaTabla/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: SolicitudMaduradorSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_madurador(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

@router.post("/DatosGraficaTablaF/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: SolicitudMaduradorSchemaF = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_madurador_filadelfia(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

@router.post("/DatosPollitos/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_pollito_data(notificacion: SolicitudMaduradorSchemaF = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_pollito(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

   

@router.post("/DatosTablaF/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data_t(notificacion: SolicitudMaduradorSchemaF = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_madurador_tabla(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

@router.get("/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def obtener_notificacion_data()->Page[DatosMadurador]:
    #convertir en json
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await obtener_madurador()
    return ResponseModel(new_notificacion, "ok")
    #return paginate(new_notificacion)

@router.post("/Tunel/", response_description="Datos del tunel agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_tunel_data(notificacion: TunelSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_tunel(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.post("/Wonderful/", response_description="Datos de wonderful agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_wonderful_data(notificacion: WonderfulSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_wonderful(notificacion)
    #return ResponseModel(new_notificacion, "ok")
    return new_notificacion


@router.get("/homologar", response_description="Datos de tunel se homologan con ztrack")
async def homologar_data_tunel():
    notificacions = await homologar_tunel_2()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/zgru1090804", response_description="Datos de tunel se homologan con ztrack")
async def homologar_zgru1090804():
    notificacions = await homologar_wonderful_zgru1090804_2()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados zgru1090804!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/zgru2009227", response_description="Datos de tunel se homologan con ztrack")
async def homologar_zgru2009227():
    notificacions = await homologar_wonderful_zgru2009227_2()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados zgru2009227!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/zgru2008220", response_description="Datos de tunel se homologan con ztrack")
async def homologar_zgru2008220():
    notificacions = await homologar_wonderful_zgru2008220_2()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados zgru2008220!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/zgru2232647", response_description="Datos de tunel se homologan con ztrack")
async def homologar_zgru2232647():
    notificacions = await homologar_wonderful_zgru2232647_2()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados zgru2232647!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/starcool_ZGRU1092515", response_description="Datos de tunel se homologan con ztrack")
async def homologar_starcool_ZGRU1092515():
    notificacions = await starcool_ZGRU1092515()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados zgru1092515!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.post("/ProcesarWonderful/", response_description="Datos necesarios para procesar datos de wonderful")
#La funcion espera "ConceptoOTSchema" SolicitudMaduradorSchema
async def procesar_wonderful_data(notificacion: ProcesarWonderfulSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await homologar_datos_wonderful(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)
