import os
from google.cloud import bigquery

# Indicamos a Python dónde está la llave
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json" # Asegúrate de que este sea el nombre de tu archivo de clave de cuenta de servicio

# Creamos el cliente de BigQuery
client = bigquery.Client(project="expenses-analyzer-492003")

# Probamos la conexión listando los datasets (aunque esté vacío)
datasets = list(client.list_datasets())

if not datasets:
    print("¡Conexión exitosa! El proyecto no tiene datasets todavía.")
else:
    print("Conexión exitosa. Datasets encontrados:")
    for ds in datasets:
        print(f"- {ds.dataset_id}")