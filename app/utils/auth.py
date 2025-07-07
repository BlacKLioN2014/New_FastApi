from fastapi import Depends, HTTPException, status
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_manager import verificar_token

security = HTTPBearer()

def obtener_usuario_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    payload = verificar_token(token)
    usuario_id = payload.get("sub")
    if usuario_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    return usuario_id
