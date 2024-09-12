from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from faker import Faker
from datetime import datetime
from app.models import Entrada, Producto, Salida
from typing import List  # Asegúrate de incluir esta línea
from . import models, schemas
from fastapi.middleware.cors import CORSMiddleware


#from app import models, schemas
from .database import SessionLocal, engine

# Inicializamos la aplicación FastAPI
app = FastAPI()

#Para permitir que React acceda a los datos de FastAPI, necesitas configurar 
# CORS en tu backend. Edita el archivo main.py en FastAPI:

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Creamos todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar Faker para generar datos de ejemplo
fake = Faker()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ruta para llenar tablas con datos aleatorios
@app.post("/fill_data/")
def fill_data(db: Session = Depends(get_db)):
    """
    Llenar las tablas de productos, clientes, entradas y salidas con datos de ejemplo.
    """
    # Crear datos de ejemplo para productos
    for _ in range():
        db_producto = models.Producto(
            nombre=fake.word(),
            descripcion=fake.text(),
            precio=fake.random_number(digits=4),
            cantidad=fake.random_number(digits=3)
        )
        db.add(db_producto)
    
    # Crear datos de ejemplo para clientes
    for _ in range():
        db_cliente = models.Cliente(
            nombre=fake.name(),
            email=fake.email(),
            telefono=fake.phone_number()
        )
        db.add(db_cliente)
    
    db.commit()

    return {"message": "Datos de ejemplo insertados exitosamente"}

# Rutas similares para gestionar productos y clientes

@app.get("/", tags=["General"])
def read_root():
    """
    Verificar que la API está funcionando correctamente.
    """
    return {"message": "API funcionando correctamente"}

# Las rutas CRUD para productos y clientes se mantienen aquí

# Ruta para crear un nuevo producto

@app.post("/fill_data/")
def fill_data(db: Session = Depends(get_db)):
    """
    Llenar las tablas de productos, clientes, entradas y salidas con datos de ejemplo.
    """
    fake = Faker()

    # Crear datos de ejemplo para productos
    for _ in range():
        db_producto = models.Producto(
            nombre=fake.word(),
            descripcion=fake.text(),
            precio=fake.random_number(digits=4),
            cantidad=fake.random_number(digits=3)
        )
        db.add(db_producto)

    # Crear datos de ejemplo para clientes
    for _ in range():
        db_cliente = models.Cliente(
            nombre=fake.name(),
            email=fake.email(),
            telefono=fake.phone_number()
        )
        db.add(db_cliente)

    db.commit()

    return {"message": "Datos de ejemplo insertados exitosamente"}

@app.post("/productos/", response_model=schemas.Producto, status_code=status.HTTP_201_CREATED)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo producto en la base de datos.
    """
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Ruta para obtener un producto por ID
@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def read_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtener los detalles de un producto específico utilizando su ID.
    """
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# Ruta para obtener una lista de todos los productos
@app.get("/productos/", response_model=List[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Obtener una lista de todos los productos, con paginación y ordenación.
    """
    productos = db.query(models.Producto).order_by(models.Producto.id).offset(skip).limit(limit).all()
    return productos

@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Obtener una lista de todos los clientes, con paginación y ordenación.
    """
    clientes = db.query(models.Cliente).order_by(models.Cliente.id).offset(skip).limit(limit).all()
    return clientes


# Ruta para actualizar un producto
@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    """
    Actualizar un producto existente en la base de datos.
    """
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Actualizamos los datos del producto
    for key, value in producto.model_dump().items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# Ruta para eliminar un producto
@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un producto de la base de datos.
    """
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return

# Rutas similares para gestionar clientes, entradas y salidas

# Ruta para crear un nuevo cliente
@app.post("/clientes/", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente en la base de datos.
    """
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Ruta para obtener un cliente por ID
@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtener los detalles de un cliente específico utilizando su ID.
    """
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

# Ruta para obtener una lista de todos los clientes
@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtener una lista de todos los clientes, con paginación y ordenación.
    """
    clientes = db.query(models.Cliente).order_by(models.Cliente.id).offset(skip).limit(limit).all()
    return clientes

# Ruta para actualizar un cliente
@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    """
    Actualizar un cliente existente en la base de datos.
    """
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizamos los datos del cliente
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)

    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Ruta para eliminar un cliente
@app.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un cliente de la base de datos.
    """
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return

# Puedes continuar creando rutas para entradas y salidas siguiendo la misma estructura

# Endpoint para obtener el reporte de entradas entre dos fechas


@app.get("/reportes/entradas")
async def get_entradas(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        # Convertir las fechas de cadena a datetime
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Consultar entradas entre las fechas especificadas
        entradas = db.query(Entrada).filter(Entrada.fecha.between(start_date_dt, end_date_dt)).all()
        
        # Devolver los datos de las entradas
        return {"data": [entrada.as_dict() for entrada in entradas]}
    except Exception as e:
        # Registrar el error para depuración
        print(f"Error en /reportes/entradas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener los datos de entradas")

# Endpoint para obtener el reporte de salidas entre dos fechas
@app.get("/reportes/salidas")
async def get_salidas(start_date: str, end_date: str, db: Session = Depends(get_db)):
    try:
        # Convertir las fechas de cadena a datetime
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Consultar salidas entre las fechas especificadas
        salidas = db.query(Salida).filter(Salida.fecha.between(start_date_dt, end_date_dt)).all()
        
        # Devolver los datos de las salidas
        return {"data": [salida.as_dict() for salida in salidas]}
    except Exception as e:
        # Registrar el error para depuración
        print(f"Error en /reportes/salidas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener los datos de salidas")
    
    @app.get("/proveedores", response_model=List[ProveedorResponse])
    async def get_proveedores():
    # Supongamos que usas SQLAlchemy para obtener datos
     proveedores = db.query(Proveedor).all()
    return proveedores
