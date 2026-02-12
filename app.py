import streamlit as st
import google.generativeai as genai
import pandas as pd
import io
import streamlit as st
import google.generativeai as genai

# Esta línea es la que conecta con el "Secret" que acabas de guardar
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
# Configuración de la página

st.set_page_config(page_title="Analizador de Sacrificios", layout="wide")
st.title("📊 Procesador de PDFs de Matadero")
st.markdown("Sube el PDF de sacrificios y obtén el análisis detallado al instante.")


# --- EL PROMPT (Tu lógica de negocio) ---
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
5. Devuelve la información estrictamente en formato de tabla Markdown.
"""

# --- INTERFAZ DE USUARIO ---
uploaded_file = st.file_uploader("Arrastra aquí el archivo PDF", type=['pdf'])

if uploaded_file is not None:
    with st.spinner('Analizando documento con Gemini...'):
        try:
            # Leer el PDF
            document_data = uploaded_file.read()
            
            # Llamada a la API de Google
            response = model.generate_content([
                SYSTEM_PROMPT,
                {"mime_type": "application/pdf", "data": document_data}
            ])
            
            # Mostrar resultado en pantalla
            st.success("¡Análisis completado!")
            st.markdown(response.text)
            
            # Botón para descargar (Opcional: aquí podrías parsear el texto a Excel real)
            st.download_button(
                label="Descargar Análisis como Texto",
                data=response.text,
                file_name="resumen_sacrificios.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Hubo un error: {e}")

st.info("Nota: Los datos se procesan de forma privada mediante la API de Google Gemini.")
