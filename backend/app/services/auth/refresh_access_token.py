from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.refresh_token import RefreshToken



def validate_refresh_token(refresh_token: str, db: Session):
    token = (
        db.query(RefreshToken)
            .filter(RefreshToken.token==refresh_token)
            .first()
    )

    # check token existance
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    
    # check expiration time
    if token.expires_at < datetime.now(timezone.utc):
        # delete old token
        db.delete(token)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired'
        )
    
    return token



def refresh_access_token(refresh_token: str, db: Session):
    # validate: expiration and existance
    token = validate_refresh_token(refresh_token=refresh_token, db=db)

    # create new access token
    new_access_token = create_access_token(data={'user_id': token.user_id})

    return {'access_token': new_access_token, 'refresh_token': token.token}