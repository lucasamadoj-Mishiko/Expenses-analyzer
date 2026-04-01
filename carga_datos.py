import pandas as pd
import os
from google.cloud import bigquery

# Configuración
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
client = bigquery.Client()
table_id = "expenses-analyzer-492003.analisis_gastos.transacciones"

try:
    # Leemos el archivo nuevo que creaste en VS Code
    # Usamos encoding='utf-8' para evitar caracteres raros de Excel
    df = pd.read_csv("test.csv", sep=',', encoding='utf-8')

    # Limpieza básica por seguridad
    df.columns = df.columns.str.strip().str.lower()

    # --- PRUEBA DE FUEGO ---
    print("--- VISTA PREVIA DE LOS DATOS ---")
    print(df.head()) 
    print(f"Columnas detectadas: {df.columns.tolist()}")
    print("---------------------------------")

    # Si 'descripcion' está en la lista, seguimos:
    if 'descripcion' in df.columns:
        # Transformaciones
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date
        df['categoria'] = 'Prueba' # Por ahora simplificamos esto
        
        # Carga
        print("Subiendo a BigQuery...")
        job = client.load_table_from_dataframe(df, table_id)
        job.result()
        print("✅ ¡POR FIN! Datos cargados con éxito.")
    else:
        print("❌ Error: Seguimos sin encontrar 'descripcion'.")
        print("Revisá que no haya espacios al principio del archivo CSV.")

except Exception as e:
    print(f"❌ ERROR: {e}")