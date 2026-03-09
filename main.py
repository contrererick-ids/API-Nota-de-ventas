from fastapi import FastAPI
from app.database import Base, engine
from app.routes import clientes, domicilios, productos, notas

# Crear tablas en la base de datos RDS al arrancar la aplicación
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Rutas
app.include_router(clientes.router)
app.include_router(domicilios.router)
app.include_router(productos.router)
app.include_router(notas.router)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
