💰 Expenses Analyzer: From PDF to BigQuery
Este proyecto nace de la necesidad de automatizar el seguimiento de finanzas personales, transformando extractos bancarios "sucios" (PDF/CSV) en datos estructurados listos para el análisis en la nube.

🚀 Overview
La aplicación utiliza Streamlit como interfaz para que cualquier usuario pueda cargar su resumen de cuenta. El motor de procesamiento limpia los datos, los categoriza automáticamente mediante lógica de palabras clave y los sincroniza con Google BigQuery para su posterior visualización en herramientas como Power BI o Looker Studio.

✨ Key Features
Intelligent PDF Extraction: Implementación de Regex (Regular Expressions) para extraer transacciones de PDFs complejos (como Mercado Pago) donde las tablas no son estándar.

Data Normalization: Limpieza automática de formatos de moneda (símbolos, separadores de miles y decimales) y estandarización de columnas.

Auto-Categorization: Sistema de clasificación de gastos basado en descripciones (Supermercado, Transporte, Servicios, etc.).

Cloud Integration: Conexión directa con el ecosistema de Google Cloud Platform (GCP).

🛠️ Tech Stack
Language: Python 3.x

Data Science: Pandas

Extraction: pdfplumber + Regular Expressions (Re)

Frontend: Streamlit

Data Warehouse: Google BigQuery

📂 Project Structure
Plaintext
├── .streamlit/          # Configuration for Dark Mode
├── app.py               # Main Streamlit application
├── requirements.txt     # Project dependencies
├── .gitignore           # Safety first! (Secrets & Data excluded)
└── README.md⚙️ Setup & Installation
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Set up your Google Cloud Service Account and save the JSON as credenciales.json.

Run the app: python -m streamlit run app.py.
