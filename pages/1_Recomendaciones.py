import streamlit as st
import sqlite3
import pandas as pd
import database_init

def obtener_recomendaciones(tipo_evento, servicios_requeridos, num_invitados, presupuesto, estilo, ubicacion):
    conn = sqlite3.connect('proveedores.db')
    recomendaciones = {}
    
    for servicio in servicios_requeridos:
        # Consultar proveedores por tipo de servicio
        df = pd.read_sql_query(
            "SELECT * FROM proveedores WHERE tipo = ?", 
            conn, 
            params=(servicio,)
        )
        
        if not df.empty:
            # Filtrar por presupuesto (asumiendo distribución del presupuesto)
            presupuesto_por_servicio = presupuesto / len(servicios_requeridos)
            df = df[df['precio_promedio'] <= presupuesto_por_servicio]
            
            # Calcular score
            df['score'] = (
                df['puntuacion'] * 0.6 +
                (1 - (df['precio_promedio'] / presupuesto_por_servicio)) * 0.4
            )
            
            # Obtener los mejores 3 proveedores para este servicio
            recomendaciones[servicio] = df.nlargest(3, 'score')
    
    conn.close()
    return recomendaciones

def main():
    st.title("Encuentra los Mejores Proveedores para tu Evento")
    
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_evento = st.selectbox(
                "Tipo de Evento:",
                ["Boda", "Cumpleaños", "Evento Corporativo", "Fiesta"]
            )
            servicios_requeridos = st.multiselect(
                "Servicios necesarios:",
                ["DJ", "Animación", "Catering", "Fotografía", "Musical", "Magia", "Decoración"]
            )
            num_invitados = st.number_input("Número de Invitados:", min_value=1)
            
        with col2:
            presupuesto = st.number_input("Presupuesto Total (ARS):", min_value=0.0)
            estilo = st.selectbox(
                "Estilo del Evento:",
                ["Moderno", "Clásico", "Infantil", "Elegante"]
            )
            ubicacion = st.text_input("Ubicación:")
        
        submitted = st.form_submit_button("Obtener Recomendaciones")
        
        if submitted and servicios_requeridos:
            recomendaciones = obtener_recomendaciones(
                tipo_evento, servicios_requeridos, num_invitados, 
                presupuesto, estilo, ubicacion
            )
            
            for servicio, proveedores in recomendaciones.items():
                st.subheader(f"Proveedores Recomendados - {servicio}")
                for _, proveedor in proveedores.iterrows():
                    with st.container():
                        st.markdown(f"""
                        ### {proveedor['nombre']}
                        - **Tipo:** {proveedor['tipo']}
                        - **Estilo:** {proveedor['estilo']}
                        - **Precio promedio:** ARS {proveedor['precio_promedio']}
                        - **Puntuación:** {proveedor['puntuacion']}/5
                        - **Ubicación:** {proveedor['ubicacion']}
                        - **Score de compatibilidad:** {proveedor['score']*100:.2f}%
                        """)
                        st.divider()

if __name__ == "__main__":
    main()