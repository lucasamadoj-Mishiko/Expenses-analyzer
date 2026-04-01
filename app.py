import streamlit as st
import pandas as pd
import os
import pdfplumber
import re
from google.cloud import bigquery

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="MP Analyzer Pro", page_icon="💳", layout="wide")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
client = bigquery.Client()
TABLE_ID = "expenses-analyzer-492003.analisis_gastos.transacciones"

# --- 2. LÓGICA DE CATEGORIZACIÓN ---
def categorizar(descripcion):
    desc = str(descripcion).lower()
    if 'rendimientos' in desc: return 'Inversión'
    if 'sweet pocket' in desc: return 'Ahorro'
    if any(w in desc for w in ['coto', 'carrefour', 'dia', 'jumbo', 'disco']): return 'Supermercado'
    if any(w in desc for w in ['pedidosya', 'rappi', 'burger', 'mcdonald', 'arnaldo', 'sicilia', 'forno rosso']): return 'Comida'
    if any(w in desc for w in ['mubi', 'netflix', 'google', 'personal', 'spotify', 'uba']): return 'Servicios/Suscripciones'
    if any(w in desc for w in ['uber', 'ypf', 'shell', 'axion', 'sube']): return 'Transporte'
    if 'farma' in desc: return 'Salud'
    return 'Otros'

# --- 3. LIMPIEZA DE MONEDA ---
def limpiar_monto(valor_str):
    if not valor_str: return 0.0
    # Quita $, espacios, y puntos de miles. Cambia coma por punto decimal.
    # Maneja casos como "$-1.499,00" o "$ 266,03"
    s = re.sub(r'[^\d,\-]', '', valor_str).replace(',', '.')
    try:
        return float(s)
    except:
        return 0.0

# --- 4. EXTRACTOR NINJA (REGEX) ---
def extraer_datos_por_texto(file):
    movimientos = []
    # Patrón: Fecha (DD-MM-AAAA) + Texto (Descripción) + ID (Números largos) + Monto ($...) + Saldo ($...)
    patron = re.compile(r'(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(\d{10,})\s+(\$?\s?-?[\d\.]+,\d{2})\s+(\$?\s?[\d\.]+,\d{2})')

    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                for linea in texto.split('\n'):
                    match = patron.search(linea)
                    if match:
                        fecha, desc, op_id, valor, saldo = match.groups()
                        movimientos.append({
                            'fecha': fecha,
                            'descripcion': desc.strip(),
                            'monto': limpiar_monto(valor)
                        })
    
    return pd.DataFrame(movimientos)

# --- 5. INTERFAZ ---
st.title("💳 Mercado Pago: Extractor Inteligente")
st.write("Analizando el periodo de: **Febrero 2026**") # Basado en tus datos [cite: 4]

archivo = st.file_uploader("Subí tu resumen de cuenta (PDF)", type=["pdf"])

if archivo:
    with st.spinner("Escaneando texto del PDF..."):
        df = extraer_datos_por_texto(archivo)
        
        if df.empty:
            st.error("❌ No pudimos encontrar movimientos con el formato esperado. Revisá si el PDF es el original.")
        else:
            # Transformaciones finales
            df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True).dt.date
            df['categoria'] = df['descripcion'].apply(categorizar)
            
            # Dashboard
            st.success(f"✅ ¡Conseguido! Se detectaron {len(df)} movimientos.")
            
            # Métricas
            ingresos = df[df['monto'] > 0]['monto'].sum()
            gastos = df[df['monto'] < 0]['monto'].sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Ingresos Totales", f"${ingresos:,.2f}")
            m2.metric("Gastos Totales", f"${abs(gastos):,.2f}", delta_color="inverse")
            m3.metric("Balance Neto", f"${(ingresos + gastos):,.2f}")

            st.divider()

            c_tabla, c_graf = st.columns([1.2, 1])
            with c_tabla:
                st.subheader("📝 Listado de Transacciones")
                st.dataframe(df, use_container_width=True)

            with c_graf:
                st.subheader("📊 Gastos por Categoría")
                df_gastos = df[df['monto'] < 0].copy()
                df_gastos['monto'] = df_gastos['monto'].abs()
                if not df_gastos.empty:
                    resumen = df_gastos.groupby('categoria')['monto'].sum().reset_index()
                    st.bar_chart(data=resumen, x='categoria', y='monto', color="#7792E3")
                else:
                    st.info("No hay gastos negativos para graficar.")

            if st.button("🚀 Sincronizar con BigQuery"):
                with st.spinner('Cargando...'):
                    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
                    client.load_table_from_dataframe(df, TABLE_ID, job_config=job_config).result()
                    st.success("¡Datos enviados a la nube!")
                    st.balloons()