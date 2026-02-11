from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        # Hacemos una consulta real para estar 100% seguros
        result = connection.execute(text("SELECT version();"))
        print("\n✅ ¡Conexión exitosa a PostgreSQL!")
        print(f"   Versión: {result.fetchone()[0]}")
except Exception as e:
    print(f"\n❌ Error de conexión: {e}")

"""
SCRIPT PARA COMPROBAR LA CONEXIÓN POSTGRESQL (versión SÍNCRONO) para Rama Develop 
------------------------------------------
Este script verifica que el 'puente' entre SQLAlchemy y PostgreSQL funcione.
1. 'from app.database import engine': Importa la configuración de conexión 
   que definimos en nuestro proyecto (usuario, puerto, BD).
2. 'engine.connect()': Intenta abrir un canal de comunicación real con el servidor.
3. 'connection.execute(...)': Ejecuta una consulta nativa de SQL (SELECT version()) 
   para confirmar que el servidor no solo nos deja entrar, sino que responde datos.

Útil para: Diagnosticar errores de contraseña, puerto o drivers (psycopg2).


SE EJECUTA EN CONSOLA COMO: pyton test_db.py
"""
