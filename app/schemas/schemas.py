from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


# Enums
class TipoDireccion(str, Enum):
    FACTURACION = "FACTURACIÓN"
    ENVIO = "ENVÍO"


# Cliente
class ClienteBase(BaseModel):
    razon_social: str
    nombre_comercial: Optional[str] = None
    rfc: str
    correo: str
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# Domicilio
class DomicilioBase(BaseModel):
    domicilio: str
    colonia: str
    municipio: str
    estado: str
    tipo: TipoDireccion
    cliente_id: int

class DomicilioCreate(DomicilioBase):
    pass

class DomicilioResponse(DomicilioBase):
    id: int

    class Config:
        from_attributes = True


# Producto
class ProductoBase(BaseModel):
    nombre: str
    unidad_medida: str
    precio_base: float

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True


# Contenido de Nota
class ContenidoNotaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class ContenidoNotaCreate(ContenidoNotaBase):
    pass

class ContenidoNotaResponse(ContenidoNotaBase):
    id: int
    importe: float
    producto: ProductoResponse

    class Config:
        from_attributes = True


# Nota
class NotaBase(BaseModel):
    folio: str
    cliente_id: int
    direccion_facturacion_id: int
    direccion_envio_id: int

class NotaCreate(NotaBase):
    contenido: List[ContenidoNotaCreate]

class NotaResponse(NotaBase):
    id: int
    total: float
    contenido: List[ContenidoNotaResponse] = []
    cliente: ClienteResponse
    direccion_facturacion: DomicilioResponse
    direccion_envio: DomicilioResponse

    class Config:
        from_attributes = True
