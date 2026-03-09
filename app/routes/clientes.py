from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Cliente
from app.schemas.schemas import ClienteCreate, ClienteResponse
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@router.get("/{id_cliente}", response_model=ClienteResponse)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=ClienteResponse)
def crear_cliente(new_cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(
        (Cliente.rfc == new_cliente.rfc) | (Cliente.correo == new_cliente.correo)
    ).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="RFC o correo ya registrado")
    cliente_to_post = Cliente(**new_cliente.model_dump())
    db.add(cliente_to_post)
    db.commit()
    db.refresh(cliente_to_post)
    return cliente_to_post


@router.put("/{id_cliente}", response_model=ClienteResponse)
def actualizar_cliente(id_cliente: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.delete("/{id_cliente}")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}
