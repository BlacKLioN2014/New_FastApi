from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.utils.jwt_manager import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

def obtener_usuario_id(token: str = Depends(oauth2_scheme)) -> str:
    payload = verificar_token(token)
    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return usuario_id
