# database_init.py
import sqlite3
import os

def init_database():
    """
    Inicializa la base de datos con la tabla de proveedores
    si no existe previamente
    """
    # Ruta completa para la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'proveedores.db')
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            estilo TEXT NOT NULL,
            precio_promedio REAL NOT NULL,
            puntuacion REAL NOT NULL,
            ubicacion TEXT NOT NULL
        )
    ''')
    
    # Verificar si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM proveedores")
    if cursor.fetchone()[0] == 0:
        # Insertar datos de prueba
        proveedores_iniciales = [
            ("DJ Carlos", "DJ", "Moderno", 500, 4.5, "Madrid"),
            ("Animaciones Pedro", "Animacion", "Infantil", 300, 4.8, "Barcelona"),
            ("Fotografía María", "Fotografia", "Elegante", 600, 4.6, "Madrid")
        ]
        
        cursor.executemany('''
            INSERT INTO proveedores 
            (nombre, tipo, estilo, precio_promedio, puntuacion, ubicacion) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', proveedores_iniciales)
    
    # Tabla de calificaciones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proveedor_id INTEGER,
            calificacion INTEGER,
            comentario TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores (id)
        )
    ''')




    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

# Llamar a la función de inicialización al importar
init_database()