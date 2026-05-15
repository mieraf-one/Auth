from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import jwt, JWTError, ExpiredSignatureError

from app.core.config import settings
from app.models.user import User
from app.database import get_db



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        user = db.query(User).filter(User.id==payload['user_id']).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Account not found'
            )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    
    return user