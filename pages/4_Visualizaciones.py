import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # En lugar de import plotly.graph_objs as go
import database_init

def obtener_datos_calificaciones():
    conn = sqlite3.connect('proveedores.db')
    
    # Consulta para obtener datos de calificaciones por tipo de servicio
    df = pd.read_sql_query("""
        SELECT 
            tipo, 
            ROUND(AVG(puntuacion), 2) as promedio_calificacion,
            COUNT(id) as total_proveedores
        FROM proveedores
        GROUP BY tipo
        ORDER BY promedio_calificacion DESC
    """, conn)
    
    # Consulta para obtener calificaciones individuales
    # Consulta para obtener calificaciones individuales con mes
    df_individual = pd.read_sql_query("""
        SELECT 
            p.nombre, 
            p.tipo, 
            ROUND(p.puntuacion, 2) as calificacion,
            COALESCE(strftime('%m', c.fecha), strftime('%m', 'now')) as mes,
            COUNT(c.id) as total_calificaciones
        FROM proveedores p
        LEFT JOIN calificaciones c ON p.id = c.proveedor_id
        GROUP BY p.id
        ORDER BY p.tipo, p.puntuacion DESC
    """, conn)
    
    # Convertir mes a nombre de mes
    meses = {
        '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr', 
        '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago', 
        '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dic'
    }
    df_individual['mes_nombre'] = df_individual['mes'].map(meses)
    
    conn.close()
    
    return df, df_individual

def crear_visualizaciones(df, df_individual):
    # Configurar layout
    st.title("Visualización de Calificaciones de Artistas")
    
    # Crear columnas
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras de promedio por tipo de servicio
        st.subheader("Calificación Promedio por Tipo de Servicio")
        fig1 = px.bar(
            df, 
            x='tipo', 
            y='promedio_calificacion',
            labels={'promedio_calificacion': 'Calificación Promedio', 'tipo': 'Tipo de Servicio'},
            color='promedio_calificacion',
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig1)
    
    with col2:
        # Gráfico de dispersión mejorado
        st.subheader("Calificaciones Individuales de Proveedores")
        
        # Colores para diferentes tipos de servicios
        colores = {
            'DJ': '#FF6384',
            'Animación': '#36A2EB',
            'Catering': '#FFCE56',
            'Fotografía': '#4BC0C0',
            'Musical': '#9966FF',
            'Magia': '#FF9F40',
            'Decoración': '#8AC926'
        }
        
        # Crear figura con más detalles
        st.subheader("Calificaciones por Mes")
        fig2 = go.Figure()
        
        # Agregar trazas para cada tipo de servicio
        for tipo in df_individual['tipo'].unique():
            datos_tipo = df_individual[df_individual['tipo'] == tipo]
            
            fig2.add_trace(go.Scatter(
                x=datos_tipo['mes_nombre'],
                y=datos_tipo['calificacion'],
                mode='markers',
                name=tipo,
                marker=dict(
                    size=datos_tipo['total_calificaciones'] * 15 + 10,
                    color=colores.get(tipo, '#7F7F7F'),
                    opacity=0.7,
                    line=dict(
                        color='white',
                        width=1
                    )
                ),
                text=datos_tipo['nombre'],
                hoverinfo='text+y',
                hovertemplate='<b>%{text}</b><br>Calificación: %{y:.2f}<extra></extra>'
            ))
        
        # Configuración del layout
        fig2.update_layout(
            title='Calificaciones de Proveedores por Mes',
            xaxis_title='Mes',
            yaxis_title='Calificación',
            yaxis=dict(range=[0, 5.5]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500,
            width=600
        )
        
        st.plotly_chart(fig2)
    
    # Tabla detallada
    st.subheader("Detalle de Calificaciones")
    df_detalle = df_individual.sort_values('calificacion', ascending=False)
    st.dataframe(df_detalle, use_container_width=True)

def main():
    # Configuración de la página
    st.set_page_config(
        page_title="Visualización de Calificaciones", 
        page_icon="📊",
        layout="wide"
    )
    
    # Estilos
    st.markdown("""
    <style>
    .stApp {
        background-color: #b606da;
    }
    .st-emotion-cache-uf99v8 {
        font-family: serif;
        color: #f8f8f9;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: serif !important;
        color: #f8f8f9 !important;
    }
    .stDataFrame {
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Obtener y mostrar datos
    df, df_individual = obtener_datos_calificaciones()
    crear_visualizaciones(df, df_individual)

if __name__ == "__main__":
    main()
