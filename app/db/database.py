from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.config import  DATABASE_URL

# Imprime para verificar que se cargó bien
print("DATABASE_URL:", DATABASE_URL)

for i, c in enumerate(DATABASE_URL):
    try:
        c.encode("utf-8")
    except UnicodeEncodeError as e:
        print(f"Caracter inválido en posición {i}: {repr(c)}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Base.metadata.create_all(bind=engine)