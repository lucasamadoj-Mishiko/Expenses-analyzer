import os
from google.cloud import bigquery
from google.api_core import exceptions

# 1. Configuración
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
client = bigquery.Client()

# Definí tus IDs aquí
project_id = "expenses-analyzer-492003"
dataset_id = f"{project_id}.analisis_gastos"
table_id = f"{dataset_id}.transacciones"

# 2. Intentar crear el Dataset con manejo de errores real
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US" 

try:
    client.get_dataset(dataset_id)  # Verificamos si realmente existe
    print(f"Confirmado: El dataset '{dataset_id}' ya existe.")
except exceptions.NotFound:
    print(f"El dataset no existe. Intentando crearlo...")
    try:
        client.create_dataset(dataset, timeout=30)
        print(f"Dataset '{dataset_id}' creado exitosamente.")
    except Exception as e:
        print(f"Error crítico al crear el dataset: {e}")
        exit() # Si no hay dataset, no podemos seguir

# 3. Definir y crear la Tabla
schema = [
    bigquery.SchemaField("fecha", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("descripcion", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("monto", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("categoria", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("banco", "STRING", mode="NULLABLE"),
]

table = bigquery.Table(table_id, schema=schema)

try:
    client.get_table(table_id)
    print(f"La tabla '{table_id}' ya existe.")
except exceptions.NotFound:
    print(f"Creando la tabla '{table_id}'...")
    client.create_table(table)
    print("Tabla creada exitosamente.")
except Exception as e:
    print(f"Hubo un error con la tabla: {e}")