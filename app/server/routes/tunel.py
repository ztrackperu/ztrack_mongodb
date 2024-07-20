from fastapi import Depends,APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
#Aqui importamos el modelo necesario para la clase 
from server.models.tunel import (
    ErrorResponseModel,
    ResponseModel,
    TunelSchema,
)
#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.tunel import (
    data_hortifruit,
    homologar_hortifruit_123321, 
    get_user,

)
from server.models_orm import contenedores as contenedorModel
from server.schemas_orm import contenedores as contenedorSchema

from server.database import SessionLocal, engine

contenedorModel.Base.metadata.create_all(bind=engine)

#aqui se definen las rutas de la API REST
router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        return 0
    return db_user

@router.post("/Hortifruit/", response_description="Datos del tunel agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_tunel_hortifruit_data(notificacion: TunelSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_hortifruit(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/HortifruitA/123321", response_description="Datos de tunel se homologan con ztrack")
async def homologar_HortifruitA_123321():
    #aqui consultamos para traer los datos de mysql con una consulta de los datos del contenedor
    dataContenido = await read_user(471)
    print('jaja')
    notificacions = await homologar_hortifruit_123321(dataContenido)
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados 123321!")
    return ResponseModel(notificacions, "Lista vacía devuelta")