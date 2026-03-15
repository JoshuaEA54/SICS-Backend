# Conexión a la base de datos
# Es el archivo que crea la conexión real entre tu aplicación y PostgreSQL. 
# Sin esto, SQLAlchemy no sabe a qué base de datos conectarse ni cómo manejar 
# las sesiones.

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from app.core.config import settings

#engine = create_engine(settings.DATABASE_URL)

#SessionLocal = sessionmaker(bind=engine)