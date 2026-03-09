from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Nota, ContenidoNota, Cliente, Domicilio
from app.schemas.schemas import NotaCreate, NotaResponse
from app.services.sns_service import enviar_notificacion
from typing import List

router = APIRouter(prefix="/notas", tags=["Notas"])


@router.get("/", response_model=List[NotaResponse])
def obtener_notas(db: Session = Depends(get_db)):
    return db.query(Nota).all()


@router.get("/{nota_id}", response_model=NotaResponse)
def obtener_nota(nota_id: int, db: Session = Depends(get_db)):
    nota = db.query(Nota).filter(Nota.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota


@router.post("/", response_model=NotaResponse)
def crear_nota(nota: NotaCreate, db: Session = Depends(get_db)):
    # Validar cliente
    cliente = db.query(Cliente).filter(Cliente.id == nota.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Validar dirección de facturación
    dir_facturacion = db.query(Domicilio).filter(
        Domicilio.id == nota.direccion_facturacion_id,
        Domicilio.cliente_id == nota.cliente_id
    ).first()
    if not dir_facturacion:
        raise HTTPException(status_code=404, detail="Dirección de facturación no encontrada")

    # Validar dirección de envío
    dir_envio = db.query(Domicilio).filter(
        Domicilio.id == nota.direccion_envio_id,
        Domicilio.cliente_id == nota.cliente_id
    ).first()
    if not dir_envio:
        raise HTTPException(status_code=404, detail="Dirección de envío no encontrada")

    total = sum(item.cantidad * item.precio_unitario for item in nota.contenido)

    # Crear nota
    nueva_nota = Nota(
        folio=nota.folio,
        cliente_id=nota.cliente_id,
        direccion_facturacion_id=nota.direccion_facturacion_id,
        direccion_envio_id=nota.direccion_envio_id,
        total=total
    )
    db.add(nueva_nota)
    db.flush()

    # Crear contenido de nota
    for item in nota.contenido:
        contenido = ContenidoNota(
            id=nueva_nota.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario,
            importe=item.cantidad * item.precio_unitario
        )
        db.add(contenido)

    db.commit()
    db.refresh(nueva_nota)

    # Notificación SNS
    enviar_notificacion(
        asunto=f"Nueva nota creada: {nueva_nota.folio}",
        mensaje=(
            f"Se ha creado la nota {nueva_nota.folio}\n"
            f"Cliente: {cliente.razon_social}\n"
            f"Total: ${nueva_nota.total:.2f}"
        )
    )

    return nueva_nota


@router.delete("/{nota_id}")
def eliminar_nota(nota_id: int, db: Session = Depends(get_db)):
    nota = db.query(Nota).filter(Nota.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    db.delete(nota)
    db.commit()
    return {"mensaje": "Nota eliminada correctamente"}
