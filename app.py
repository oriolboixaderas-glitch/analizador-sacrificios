import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Analizador de Sacrificios", layout="wide")
st.title("📊 Procesador de PDFs de Matadero")

# Configuración de la API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Falta la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Forzamos la configuración
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usamos el modelo con su nombre técnico completo para evitar el 404
MODEL_NAME = 'models/gemini-1.5-flash'

try:
    model = genai.GenerativeModel(model_name=MODEL_NAME)
except Exception as e:
    st.error(f"No se pudo inicializar el modelo: {e}")
    st.stop()

SYSTEM_PROMPT = """
Analiza este documento PDF de sacrificios de animales.
1. Extrae cada ganadero y sus animales asociados.
2. Calcula los costes (MER, Sacrificio, Interprofesional) e ingresos (Menuts, Cuero).
3. Devuelve una tabla resumen por ganadero con el beneficio neto final.
Sé preciso con los números.
"""

uploaded_file = st.file_uploader("Sube el PDF de sacrificios", type=['pdf'])

if uploaded_file is not None:
    with st.spinner('Procesando con Gemini 1.5 Flash...'):
        try:
            # Preparar el archivo para el envío
            file_data = uploaded_file.getvalue()
            
            # Crear el contenido para la API
            content_payload = [
                SYSTEM_PROMPT,
                {"mime_type": "application/pdf", "data": file_data}
            ]
            
            # Realizar la llamada
            response = model.generate_content(content_payload)
            
            if response.text:
                st.success("¡Análisis completado!")
                st.markdown(response.text)
            else:
                st.warning("El modelo no devolvió resultados. Inténtalo de nuevo.")
                
        except Exception as e:
            st.error(f"Error específico: {e}")
            st.info("Nota: Si persiste el error 404, intenta 'Reboot App' en el menú de Streamlit.")
