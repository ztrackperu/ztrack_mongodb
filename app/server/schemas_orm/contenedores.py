from pydantic import BaseModel

class SchemasContenedorBase(BaseModel):
    nombre_contenedor: str
    #name: str



class SchemasContenedorCreate(SchemasContenedorBase):
    pass 

class SchemasContenedor(SchemasContenedorBase):
    id : int
    #is_active : bool

    class Config:
        orm_model = True
