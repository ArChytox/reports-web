from sqlalchemy import create_engine  # Importamos la función para crear un motor de base de datos
from sqlalchemy.ext.declarative import declarative_base  # Importamos la función para crear una clase base para los modelos
from sqlalchemy.orm import sessionmaker  # Importamos la función para crear sesiones de la base de datos


# Definimos la URL de la base de datos. En este caso, usamos pyodbc para conectar a SQL Server con autenticación de Windows.
SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://@ARCHYSS\\BD1/Prueba1?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

# Creamos el motor de la base de datos usando la URL definida.
# El motor es responsable de gestionar la conexión a la base de datos.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos una sesión local que se utiliza para realizar transacciones con la base de datos.
# Autocommit=False significa que los cambios no se confirmarán automáticamente, lo que nos permite manejar transacciones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos una clase base que utilizarán los modelos para heredar la funcionalidad de SQLAlchemy.
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)