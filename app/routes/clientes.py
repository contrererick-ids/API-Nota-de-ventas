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


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(
        (Cliente.rfc == cliente.rfc) | (Cliente.correo == cliente.correo)
    ).first()
    if db_cliente:
        raise HTTPException(status_code=400, detail="RFC o correo ya registrado")
    nuevo_cliente = Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}
