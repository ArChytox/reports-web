import pyodbc

# Configura tu cadena de conexión
conn_str = (
    "DRIVER={SQL Server};"  # Puedes usar {ODBC Driver 17 for SQL Server} si es aplicable
    "SERVER=ARCHYSS\\BD1;"  # Nombre del servidor y la instancia
    "DATABASE=Prueba1;"  # Nombre de la base de datos
    "Trusted_Connection=yes;"  # Usar autenticación de Windows
)

try:
    # Intenta conectarte a la base de datos
    with pyodbc.connect(conn_str) as conn:
        print("Conexión exitosa")
        # Ejecuta una consulta simple para verificar
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        if row:
            print("Consulta ejecutada exitosamente:", row[0])
        else:
            print("No se encontraron resultados para la consulta.")
except Exception as e:
    print(f"Error al conectar: {e}")