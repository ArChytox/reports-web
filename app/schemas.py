from pydantic import BaseModel
from typing import Optional

# Esquema base para el Proveedor
class ProveedorBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: str
    email: str

# Esquema de respuesta para Proveedor
class ProveedorResponse(BaseModel):
    id: int
    nombre: str
    direccion: Optional[str] = None  # Maneja 'None' en la dirección
    telefono: Optional[str] = None
    email: Optional[str] = None

    @classmethod
    def from_orm(cls, obj):
        obj.direccion = obj.direccion or ""  # Convierte None a una cadena vacía
        return super().from_orm(obj)

    class Config:
        from_attributes = True  # Compatible con SQLAlchemy y Pydantic V2


# Esquema base para Producto (entrada de datos)
class ProductoBase(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]
    stock: Optional[int]

# Esquema para crear un Producto
class ProductoCreate(ProductoBase):
    pass

# Esquema para la respuesta de Producto (incluyendo el ID)
class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True # Habilita la compatibilidad con modelos ORM como SQLAlchemy

# Esquema base de Cliente (utilizado para actualizar o crear clientes)
class ClienteBase(BaseModel):
    nombre: str
    direccion: Optional[str]
    telefono: Optional[str]
    email: Optional[str]

class Config:
    from_attributes = True # Permite que Pydantic trabaje con objetos ORM de SQLAlchemy

# Esquema utilizado para crear un cliente (no incluye el id)
class ClienteCreate(ClienteBase):
    pass

# Esquema utilizado para respuestas de Cliente (incluye el id)
class Cliente(ClienteBase):
    id: int