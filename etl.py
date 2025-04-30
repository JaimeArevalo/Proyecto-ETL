#!/usr/bin/env python3
"""
ETL Básico en Python
===================
Este script implementa un proceso ETL básico:
- Extract: Extrae datos de una fuente (archivo CSV, base de datos, API)
- Transform: Limpia y transforma los datos
- Load: Carga los datos transformados en el destino
"""

import pandas as pd
import logging
import os
from datetime import datetime
import requests
from sqlalchemy import create_engine

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_log.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ETL')

class ETLPipeline:
    def __init__(self):
        """Inicializa el pipeline ETL."""
        self.data = None
        self.config = {
            'input_path': 'data/input/',
            'output_path': 'data/output/',
            'db_connection': 'sqlite:///data/etl.db'
        }
        # Crear directorios si no existen
        os.makedirs(self.config['input_path'], exist_ok=True)
        os.makedirs(self.config['output_path'], exist_ok=True)
        
    def extract_from_csv(self, filename):
        """Extrae datos desde un archivo CSV."""
        try:
            file_path = os.path.join(self.config['input_path'], filename)
            logger.info(f"Extrayendo datos de {file_path}")
            self.data = pd.read_csv(file_path)
            logger.info(f"Extraídos {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error en la extracción CSV: {str(e)}")
            return False
    
    def extract_from_database(self, query, connection_string=None):
        """Extrae datos desde una base de datos SQL."""
        try:
            connection_string = connection_string or self.config['db_connection']
            logger.info(f"Extrayendo datos de BD: {query}")
            engine = create_engine(connection_string)
            self.data = pd.read_sql_query(query, engine)
            logger.info(f"Extraídos {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error en extracción BD: {str(e)}")
            return False
    
    def extract_from_api(self, url, params=None, headers=None):
        """Extrae datos desde una API REST."""
        try:
            logger.info(f"Extrayendo datos de API: {url}")
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.data = pd.DataFrame(data)
            logger.info(f"Extraídos {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error en extracción API: {str(e)}")
            return False
    
    def transform(self):
        """Transforma los datos extraídos."""
        if self.data is None or self.data.empty:
            logger.error("No hay datos para transformar")
            return False
        
        try:
            logger.info("Iniciando transformación")
            # Eliminar filas con valores nulos
            initial_rows = len(self.data)
            self.data = self.data.dropna()
            
            # Convertir columnas de fecha si existen
            if 'fecha' in self.data.columns:
                self.data['fecha'] = pd.to_datetime(self.data['fecha'], errors='coerce')
                self.data = self.data.dropna(subset=['fecha'])
            
            # Normalizar texto
            for col in self.data.select_dtypes(include=['object']).columns:
                self.data[col] = self.data[col].str.strip().str.lower()
            
            logger.info(f"Transformación completada: {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error en transformación: {str(e)}")
            return False
    
    def load_to_csv(self, filename):
        """Carga los datos transformados a un archivo CSV."""
        if self.data is None or self.data.empty:
            logger.error("No hay datos para cargar")
            return False
        
        try:
            file_path = os.path.join(self.config['output_path'], filename)
            logger.info(f"Cargando datos a {file_path}")
            self.data.to_csv(file_path, index=False)
            logger.info(f"Datos cargados: {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error al cargar a CSV: {str(e)}")
            return False
    
    def load_to_database(self, table_name, connection_string=None, if_exists='replace'):
        """Carga los datos transformados a una base de datos SQL."""
        if self.data is None or self.data.empty:
            logger.error("No hay datos para cargar")
            return False
        
        try:
            connection_string = connection_string or self.config['db_connection']
            logger.info(f"Cargando datos a tabla {table_name}")
            engine = create_engine(connection_string)
            self.data.to_sql(table_name, engine, if_exists=if_exists, index=False)
            logger.info(f"Datos cargados a BD: {len(self.data)} registros")
            return True
        except Exception as e:
            logger.error(f"Error al cargar a BD: {str(e)}")
            return False
    
    def run_pipeline(self, extract_method='csv', transform=True, load_method='csv', **kwargs):
        """Ejecuta el pipeline ETL completo."""
        try:
            logger.info("Iniciando pipeline ETL")
            
            # Extracción
            extract_success = False
            if extract_method == 'csv':
                extract_success = self.extract_from_csv(kwargs.get('input_file', 'data.csv'))
            elif extract_method == 'database':
                extract_success = self.extract_from_database(
                    kwargs.get('query', 'SELECT * FROM data'),
                    kwargs.get('db_connection')
                )
            elif extract_method == 'api':
                extract_success = self.extract_from_api(
                    kwargs.get('url'),
                    kwargs.get('params'),
                    kwargs.get('headers')
                )
            
            if not extract_success:
                logger.error("Extracción fallida")
                return False
            
            # Transformación
            if transform:
                if not self.transform():
                    logger.error("Transformación fallida")
                    return False
            
            # Carga
            if load_method == 'csv':
                if not self.load_to_csv(kwargs.get('output_file', 'processed_data.csv')):
                    logger.error("Carga a CSV fallida")
                    return False
            elif load_method == 'database':
                if not self.load_to_database(
                    kwargs.get('table_name', 'processed_data'),
                    kwargs.get('db_connection'),
                    kwargs.get('if_exists', 'replace')
                ):
                    logger.error("Carga a BD fallida")
                    return False
            
            logger.info("Pipeline ETL completado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error general en ETL: {str(e)}")
            return False

# Ejemplo de uso
if __name__ == "__main__":
    etl = ETLPipeline()
    # CSV a CSV
    etl.run_pipeline(
        extract_method='csv',
        input_file='datos_crudos.csv',
        transform=True,
        load_method='csv',
        output_file='datos_procesados.csv'
    )