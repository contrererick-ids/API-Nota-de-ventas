from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Domicilio, Cliente
from app.schemas.schemas import DomicilioCreate, DomicilioResponse
from typing import List

router = APIRouter(prefix="/domicilios", tags=["Domicilios"])


@router.get("/", response_model=List[DomicilioResponse])
def obtener_domicilios(db: Session = Depends(get_db)):
    return db.query(Domicilio).all()


@router.get("/{domicilio_id}", response_model=DomicilioResponse)
def obtener_domicilio(domicilio_id: int, db: Session = Depends(get_db)):
    domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if not domicilio:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    return domicilio

# GET adicional para obtener todos los domicilios de un cliente, servirá después al momento de crear las Notas de venta
@router.get("/cliente/{cliente_id}", response_model=List[DomicilioResponse])
def obtener_domicilios_por_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db.query(Domicilio).filter(Domicilio.cliente_id == cliente_id).all()


@router.post("/", response_model=DomicilioResponse)
def crear_domicilio(domicilio: DomicilioCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == domicilio.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    nuevo_domicilio = Domicilio(**domicilio.model_dump())
    db.add(nuevo_domicilio)
    db.commit()
    db.refresh(nuevo_domicilio)
    return nuevo_domicilio


@router.put("/{domicilio_id}", response_model=DomicilioResponse)
def actualizar_domicilio(domicilio_id: int, domicilio: DomicilioCreate, db: Session = Depends(get_db)):
    db_domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if not db_domicilio:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    for key, value in domicilio.model_dump().items():
        setattr(db_domicilio, key, value)
    db.commit()
    db.refresh(db_domicilio)
    return db_domicilio


@router.delete("/{domicilio_id}")
def eliminar_domicilio(domicilio_id: int, db: Session = Depends(get_db)):
    db_domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if not db_domicilio:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    db.delete(db_domicilio)
    db.commit()
    return {"mensaje": "Domicilio eliminado correctamente"}
