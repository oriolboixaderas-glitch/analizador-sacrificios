import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Sacrificios", layout="wide")
st.title("📊 Procesador de PDFs de Matadero")

# 2. Configuración de la API
try:
    # Intentamos obtener la clave de los secrets
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("No se encontró la clave GEMINI_API_KEY en los Secrets de Streamlit.")
        st.stop()

    genai.configure(api_key=api_key)
    
    # Probamos con el nombre de modelo más compatible
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# 3. Instrucciones de análisis
SYSTEM_PROMPT = """
Analiza el PDF de sacrificios adjunto. 
Extrae los datos de los ganaderos, pesos de canal, pesos de cuero y edades.
Calcula MER, Sacrificio, Interprofesional, Menuts y Cuero según las reglas de precios establecidas.
Presenta un resumen por ganadero con animales totales, kg, costes, ingresos y beneficio final.
Devuelve el resultado en una tabla Markdown clara.
"""

# 4. Interfaz de usuario
uploaded_file = st.file_uploader("Sube el PDF de sacrificios", type=['pdf'])

if uploaded_file is not None:
    with st.spinner('Procesando documento...'):
        try:
            # Convertimos el PDF a bytes para enviarlo
            file_bytes = uploaded_file.read()
            
            # Realizamos la petición
            response = model.generate_content([
                SYSTEM_PROMPT,
                {"mime_type": "application/pdf", "data": file_bytes}
            ])
            
            if response.text:
                st.success("Análisis finalizado")
                st.markdown(response.text)
            else:
                st.warning("El modelo no devolvió texto. Revisa el contenido del PDF.")
                
        except Exception as e:
            # Si falla el modelo flash, intentamos avisar del error específico
            st.error(f"Error al procesar el contenido: {e}")
