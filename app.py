import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Sacrificios", layout="wide")
st.title("📊 Procesador de PDFs de Matadero")

# 2. Configuración de la API (Usando tus Secrets de Streamlit)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # AQUÍ DEFINIMOS EL MODELO (esto es lo que faltaba o estaba mal puesto)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
except Exception as e:
    st.error("Error en la configuración de la API. Revisa tus Secrets en Streamlit.")
    st.stop()

# 3. El Prompt con las instrucciones de cálculo
SYSTEM_PROMPT = """
Actúa como un experto en extracción de datos de matadero.
Instrucciones:
1. Lee todo el PDF, identifica ganaderos y agrupa sus animales.
2. Para cada animal extrae: ID Canal (5 dígitos), Peso Canal (segundo decimal de la línea), Peso Cuero (número decimal único), Edad (+12 o -12).
3. Cálculos: 
   - MER: +12=9€, -12=6€. 
   - SACRIFICIO: peso canal * 0,2396€. 
   - INTERPROF: 0,50€. 
   - MENUT: 38€.
   - CUERO: >=41kg: 0,85€/kg; 36-40.9kg: 1,05€/kg; <36kg: 1,65€/kg.
4. Calcula por ganadero: Kg totales, Costes, Ingresos, Decomisos y Beneficio.
5. Devuelve la información en una tabla Markdown clara y un resumen final.
"""

# 4. Interfaz de subida de archivos
uploaded_file = st.file_uploader("Sube el PDF de sacrificios", type=['pdf'])

if uploaded_file is not None:
    with st.spinner('Gemini está analizando el PDF...'):
        try:
            # Leemos el archivo
            document_data = uploaded_file.read()
            
            # Usamos el modelo que definimos arriba
            response = model.generate_content([
                SYSTEM_PROMPT,
                {"mime_type": "application/pdf", "data": document_data}
            ])
            
            st.success("¡Análisis listo!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Hubo un error al procesar: {e}")
