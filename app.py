import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Analizador de Sacrificios", layout="wide")
st.title("📊 Procesador de PDFs de Matadero")

# Configuración de la API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Falta la clave GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usamos el nombre de modelo más estándar posible
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
Analiza el PDF adjunto. 
1. Extrae datos de ganaderos y animales.
2. Calcula: MER (+12=9€, -12=6€), Sacrificio (Peso*0.2396€), Interprof (0.50€), Menut (38€ ingreso).
3. Calcula Cuero (ingreso): >=41kg: 0.85€/kg; 36-40.9kg: 1.05€/kg; <36kg: 1.65€/kg.
4. Muestra tabla resumen por ganadero con beneficio neto.
"""

uploaded_file = st.file_uploader("Sube el PDF de sacrificios", type=['pdf'])

if uploaded_file is not None:
    with st.spinner('Procesando...'):
        try:
            # Leemos el archivo
            pdf_parts = [
                {
                    "mime_type": "application/pdf",
                    "data": uploaded_file.getvalue()
                }
            ]
            
            # Generamos contenido
            response = model.generate_content([SYSTEM_PROMPT, pdf_parts[0]])
            
            st.success("¡Completado!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error específico: {e}")
            st.info("Si el error persiste, intenta generar una nueva API Key en Google AI Studio.")
