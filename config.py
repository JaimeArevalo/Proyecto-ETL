"""
Archivo de configuración para el ETL
"""

# Rutas de directorios
INPUT_DIR = 'data/input/'
OUTPUT_DIR = 'data/output/'

# Configuración de base de datos
DATABASE = {
    'sqlite': 'sqlite:///data/etl.db',
    'mysql': 'mysql+pymysql://user:password@localhost/etl_db',
    'postgres': 'postgresql://user:password@localhost:5432/etl_db'
}

# Configuración de API
API = {
    'url': 'https://api.ejemplo.com/datos',
    'token': 'tu_token_aqui',
    'headers': {
        'Authorization': 'Bearer tu_token_aqui',
        'Content-Type': 'application/json'
    }
}

# Configuración de transformación
TRANSFORMACIONES = {
    'eliminar_nulos': True,
    'convertir_fechas': True,
    'normalizar_texto': True
}