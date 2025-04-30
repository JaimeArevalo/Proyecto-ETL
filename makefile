.PHONY: build run csv-to-csv db-to-db api-to-csv clean

# Construir la imagen
build:
	docker-compose build

# Ejecutar el ejemplo por defecto (CSV a CSV)
run:
	docker-compose up

# Ejecutar específicamente el ejemplo CSV a CSV
csv-to-csv:
	docker-compose run etl python -c "from ejemplo_uso import ejemplo_csv_a_csv; ejemplo_csv_a_csv()"

# Ejecutar específicamente el ejemplo BD a BD
db-to-db:
	docker-compose run etl python -c "from ejemplo_uso import ejemplo_bd_a_bd; ejemplo_bd_a_bd()"

# Ejecutar específicamente el ejemplo API a CSV
api-to-csv:
	docker-compose run etl python -c "from ejemplo_uso import ejemplo_api_a_csv; ejemplo_api_a_csv()"

# Limpiar contenedores y volúmenes
clean:
	docker-compose down
	docker-compose rm -f