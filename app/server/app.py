from fastapi import FastAPI

#from server.routes.usuarios import router as UsuariosRouter
from server.routes.madurador import router as MaduradorRouter

app = FastAPI(
    title="Integracion ZTRACK MONGODB",
    summary="Modulos de datos bidireccional",
    version="0.0.1",

)

#añadir el conjunto de rutas de notificaciones
#app.include_router(UsuariosRouter, tags=["usuarios"], prefix="/usuarios")
app.include_router(MaduradorRouter, tags=["maduradores"], prefix="/maduradores")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app ztrack by mongodb!"}
