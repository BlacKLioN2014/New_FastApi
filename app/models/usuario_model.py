from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    contrasena = Column(String, nullable=False)

