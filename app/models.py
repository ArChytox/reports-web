from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base  # Asegúrate de importar correctamente 'Base'
from datetime import datetime
from typing import Optional
import app.models 


# Modelo para la tabla 'productos'
class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    precio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    entradas: Mapped[list["Entrada"]] = relationship("Entrada", back_populates="producto")
    salidas: Mapped[list["Salida"]] = relationship("Salida", back_populates="producto")

# Modelo para la tabla 'clientes'
class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(VARCHAR, nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(VARCHAR, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(VARCHAR, nullable=True)

    salidas: Mapped[list["Salida"]] = relationship("Salida", back_populates="cliente")

# Modelo para la tabla 'entradas'
class Entrada(Base):
    __tablename__ = 'entradas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey('productos.id'))
    cantidad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fecha: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación con 'Producto'
    producto: Mapped["Producto"] = relationship("Producto", back_populates="entradas")

    # Método as_dict no es necesario si usas Pydantic, pero si lo necesitas:
    def as_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'fecha': self.fecha.isoformat() if self.fecha else None
        }

producto: Mapped["Producto"] = relationship("Producto", back_populates="entradas")

# Modelo para la tabla 'salidas'
class Salida(Base):
    __tablename__ = "salidas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey('productos.id'))
    cliente_id: Mapped[int] = mapped_column(Integer, ForeignKey('clientes.id'))
    cantidad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fecha: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    producto: Mapped["Producto"] = relationship("Producto", back_populates="salidas")
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="salidas")

    def as_dict(self):
        """Este método convierte el objeto 'Salida' a un diccionario."""
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cliente_id': self.cliente_id,
            'cantidad': self.cantidad,
            'fecha': self.fecha
        }

