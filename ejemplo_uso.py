#!/usr/bin/env python3
"""
Ejemplo de uso del ETL
"""

from etl import ETLPipeline

def ejemplo_csv_a_csv():
    """Procesa un CSV y guarda el resultado en otro CSV"""
    etl = ETLPipeline()
    etl.run_pipeline(
        extract_method='csv',
        input_file='datos_crudos.csv',
        transform=True,
        load_method='csv',
        output_file='datos_procesados.csv'
    )

def ejemplo_bd_a_bd():
    """Extrae datos de una BD y los guarda en otra tabla"""
    etl = ETLPipeline()
    etl.run_pipeline(
        extract_method='database',
        query='SELECT * FROM ventas WHERE fecha > "2023-01-01"',
        db_connection='sqlite:///data/ventas.db',
        transform=True,
        load_method='database',
        table_name='ventas_procesadas'
    )

def ejemplo_api_a_csv():
    """Obtiene datos de una API y los guarda en CSV"""
    etl = ETLPipeline()
    etl.run_pipeline(
        extract_method='api',
        url='https://api.ejemplo.com/datos',
        params={'limite': 1000},
        headers={'Authorization': 'Bearer token123'},
        transform=True,
        load_method='csv',
        output_file='datos_api.csv'
    )

if __name__ == "__main__":
    # Ejecutar el ejemplo que necesites
    ejemplo_csv_a_csv()
    # ejemplo_bd_a_bd()
    # ejemplo_api_a_csv()