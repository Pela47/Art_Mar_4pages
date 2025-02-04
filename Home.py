import streamlit as st
import database_init  # Esto ya ejecutará init_database()

# Configura la página principal como una página de landing o redirección
st.set_page_config(
    page_title="Artistas De Mar Event Solutions", 
    page_icon="🎉",
    layout="centered"
)

st.markdown("""
    <style>
    /* Configuración principal */
    .stApp {
        background-color: #b606da;
    }
    
    /* Estilo del texto */
    .st-emotion-cache-uf99v8 {
        font-family: serif;
        color: #f8f8f9;
    }
    
    /* Estilo de headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: serif !important;
        color: #f8f8f9 !important;
    }
    
    /* Estilo para textos normales */
    p, label, .stMarkdown {
        font-family: serif !important;
        color: #f8f8f9 !important;
    }
    
    /* Estilo para botones */
    .stButton > button {
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
        font-family: serif !important;
    }
    
    .stButton > button:hover {
        background-color: #444444 !important;
    }
    
    /* Eliminar elementos por defecto */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("Bienvenido a Artistas De Mar")
st.write("Por favor, selecciona una opción en el menú lateral.")