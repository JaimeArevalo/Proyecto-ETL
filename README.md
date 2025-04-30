# ETL Básico en Docker

Este proyecto implementa un ETL (Extract, Transform, Load) básico en Python, empaquetado en Docker para facilitar su despliegue y ejecución en cualquier entorno.

## Estructura del proyecto

```
etl-docker/
│
├── data/
│   ├── input/          # Carpeta para los archivos de entrada
│   │   └── datos_crudos.csv
│   │
│   └── output/         # Carpeta para los archivos procesados
│
├── etl.py              # Clase principal ETLPipeline
├── config.py           # Configuraciones
├── ejemplo_uso.py      # Ejemplos de uso
├── requirements.txt    # Dependencias
├── Dockerfile          # Instrucciones para crear la imagen
├── docker-compose.yml  # Configuración de servicios
└── Makefile            # Comandos útiles
```

## Requisitos

- Docker
- Docker Compose

## Cómo usar

### 1. Construir la imagen

```bash
make build
```

o manualmente:

```bash
docker-compose build
```

### 2. Ejecutar el ETL

```bash
make run
```

o manualmente:

```bash
docker-compose up
```

### 3. Ejecutar ejemplos específicos

CSV a CSV:
```bash
make csv-to-csv
```

Base de datos a base de datos:
```bash
make db-to-db
```

API a CSV:
```bash
make api-to-csv
```

### 4. Limpiar contenedores

```bash
make clean
```

## Personalización

1. Modifica los archivos de entrada en la carpeta `data/input/`
2. Ajusta la configuración en `config.py`
3. Personaliza las transformaciones en el método `transform()` de la clase `ETLPipeline`

## Notas

- Los datos procesados se guardarán en `data/output/`
- Los logs se muestran en la consola mientras se ejecuta el contenedor