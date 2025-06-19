import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = "postgresql://usuario:Mepiel24@127.0.0.1:5432/mejora_continua"
DATABASE_URL = os.getenv("DATABASE_URL")

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