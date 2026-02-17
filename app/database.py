from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base 
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://admin:123@localhost:5433/bookcircle" <== CASCARÓN 
# SQLALCHEMY_DATABASE_URL = "postgresql://Admin:kaisql@localhost:5432/bookcircle" <== VERSION SÍNCRONA ADAPTADA

"""
BITÁCORA DE MIGRACIÓN: ASÍNCRONO - 06 Feb
--------------------------------------
* Comando ejecutado: pip install asyncpg
* Propósito: 
SQLAlchemy por sí solo no sabe cómo conectarse físicamente a las bases de datos; 
necesita un 'driver'. Para PostgreSQL síncrono usábamos 'psycopg2', pero para 
la arquitectura async/await de esta rama necesitamos 'asyncpg'.

Sin este driver, el prefijo 'postgresql+asyncpg://' en la URL de conexión 
provocaría un error de 'ModuleNotFoundError'.
"""
#SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///database.db" <== VERSION ASYNC DE EJEMPLO: SESION 06 FEBRERO
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://admin:kaisql@localhost:5432/bookcircle" # <== VERSION ASYNC ADAPTADA


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, 
                            class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
    