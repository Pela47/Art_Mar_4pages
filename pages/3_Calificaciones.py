import streamlit as st
import sqlite3
import pandas as pd
import database_init

def guardar_calificacion(proveedor_id, calificacion, comentario):
    conn = sqlite3.connect('proveedores.db')
    c = conn.cursor()
    try:
        # Guardar la calificación individual
        c.execute('''
            INSERT INTO calificaciones 
            (proveedor_id, calificacion, comentario)
            VALUES (?, ?, ?)
        ''', (proveedor_id, calificacion, comentario))
        
        # Actualizar el promedio en la tabla de proveedores
        c.execute('''
            UPDATE proveedores 
            SET puntuacion = (
                SELECT AVG(calificacion) 
                FROM calificaciones 
                WHERE proveedor_id = ?
            )
            WHERE id = ?
        ''', (proveedor_id, proveedor_id))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {str(e)}")
        return False
    finally:
        conn.close()

def mostrar_ranking():
    conn = sqlite3.connect('proveedores.db')
    ranking = pd.read_sql_query("""
        SELECT 
            p.nombre,
            p.tipo,
            p.puntuacion,
            COUNT(c.id) as total_calificaciones,
            GROUP_CONCAT(c.comentario, '|') as ultimos_comentarios
        FROM proveedores p
        LEFT JOIN calificaciones c ON p.id = c.proveedor_id
        GROUP BY p.id
        ORDER BY p.puntuacion DESC
    """, conn)
    conn.close()
    
    return ranking

def main():
    st.title("Calificaciones y Rankings")
    
    tab1, tab2 = st.tabs(["Calificar Proveedor", "Ver Rankings"])
    
    with tab1:
        st.header("Califica tu Experiencia")
        
        with st.form("rating_form"):
            # Obtener lista de proveedores
            conn = sqlite3.connect('proveedores.db')
            proveedores = pd.read_sql_query(
                "SELECT id, nombre, tipo FROM proveedores", 
                conn
            )
            conn.close()
            
            proveedor = st.selectbox(
                "Selecciona el Proveedor:",
                options=proveedores['nombre'].tolist()
            )
            
            calificacion = st.slider(
                "Calificación:",
                min_value=1,
                max_value=5,
                value=5,
                help="1 = Malo, 5 = Excelente"
            )
            
            comentario = st.text_area(
                "Comentario:",
                help="Comparte tu experiencia"
            )
            
            submitted = st.form_submit_button("Enviar Calificación")
            
            if submitted:
                proveedor_id = proveedores[
                    proveedores['nombre'] == proveedor
                ]['id'].iloc[0]
                
                if guardar_calificacion(proveedor_id, calificacion, comentario):
                    st.success("¡Gracias por tu calificación!")
                    st.balloons()
    
    with tab2:
        st.header("Ranking de Proveedores")
        ranking = mostrar_ranking()
        
        for _, row in ranking.iterrows():
            with st.container():
                st.markdown(f"""
                ### {row['nombre']} - {row['tipo']}
                **Puntuación:** {row['puntuacion']:.1f}/5 ({row['total_calificaciones']} calificaciones)
                """)
                
                if pd.notna(row['ultimos_comentarios']):
                    st.markdown("**Últimos comentarios:**")
                    comentarios = row['ultimos_comentarios'].split('|')[:3]  # Mostrar últimos 3
                    for comentario in comentarios:
                        st.markdown(f"- _{comentario}_")
                
                st.divider()

if __name__ == "__main__":
    main()