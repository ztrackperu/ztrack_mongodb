from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination
from fastapi.middleware.cors import CORSMiddleware
#from server.routes.usuarios import router as UsuariosRouter
from server.routes.madurador import router as MaduradorRouter
from server.routes.tunel import router as HortifruitRouter
from server.routes.starcool import router as StarcoolRouter

app = FastAPI(
    title="Integracion ZTRACK MONGODB",
    summary="Modulos de datos bidireccional",
    version="0.0.1",
)

#origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    #allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#añadir el conjunto de rutas de notificaciones
#app.include_router(UsuariosRouter, tags=["usuarios"], prefix="/usuarios")
app.include_router(MaduradorRouter, tags=["maduradores"], prefix="/maduradores")
app.include_router(HortifruitRouter, tags=["Tunel"], prefix="/tunel")
app.include_router(StarcoolRouter, tags=["StarCool"], prefix="/starcool")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app ztrack by mongodb!"}

add_pagination(app)