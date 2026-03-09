from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String(150), nullable=False)
    nombre_comercial = Column(String(150), nullable=True)
    rfc = Column(String(13), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)

    domicilios = relationship("Domicilio", back_populates="cliente")
    notas = relationship("Nota", back_populates="cliente")


class Domicilio(Base):
    __tablename__ = "domicilios"

    id = Column(Integer, primary_key=True, index=True)
    domicilio = Column(String(200), nullable=False)
    colonia = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    tipo = Column(Enum("FACTURACIÓN", "ENVÍO"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="domicilios")


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    unidad_medida = Column(String(50), nullable=False)
    precio_base = Column(Float, nullable=False)


class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    folio = Column(String(50), unique=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    direccion_facturacion_id = Column(Integer, ForeignKey("domicilios.id"), nullable=False)
    direccion_envio_id = Column(Integer, ForeignKey("domicilios.id"), nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="notas")
    direccion_facturacion = relationship("Domicilio", foreign_keys=[direccion_facturacion_id])
    direccion_envio = relationship("Domicilio", foreign_keys=[direccion_envio_id])
    contenido = relationship("ContenidoNota", back_populates="nota", cascade="all, delete-orphan")


class ContenidoNota(Base):
    __tablename__ = "contenido_nota"

    id = Column(Integer, ForeignKey("notas.id"), primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    importe = Column(Float, nullable=False)

    nota = relationship("Nota", back_populates="contenido")
    producto = relationship("Producto")
