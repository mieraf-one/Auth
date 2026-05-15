from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.auth.delete_user import delete_user
from app.services.auth.forgot_password import send_reset_code, update_reset_password
from app.services.auth.refresh_access_token import refresh_access_token
from app.services.auth.logout import logout_user
from app.services.auth.send_email_verification import send_code
from app.services.auth.update.update_email import email_update
from app.services.auth.update.update_password import password_update
from app.services.auth.update.update_username import username_update
from app.services.auth.verify_email_code import verify_code
from app.dependencies.auth import get_current_user
from app.services.auth.signup import create_user
from app.services.auth.login import login_user
from app.database import get_db
from app.models.user import User
from app.schemas import auth



router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

# -------------------------------------------------------
#                       SIGN UP
# -------------------------------------------------------
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=auth.SignupOut)
def signup_route(data: auth.SignupIn, db: Session = Depends(get_db)):
    return create_user(data, db)


# -------------------------------------------------------
#                       LOGIN
# -------------------------------------------------------
@router.post('/login', response_model=auth.LoginOut)
def login_route(data: auth.LoginIn, db: Session = Depends(get_db)):
    return login_user(data=data, db=db)


# -------------------------------------------------------
#                      LOG OUT
# -------------------------------------------------------
@router.delete('/logout')
def logout_route(data: auth.RefreshToken, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logout_user(refresh_token=data.refresh_token, current_user=current_user, db=db)
    return {"message": "logged out"}


# -------------------------------------------------------
#                       PROFILE
# -------------------------------------------------------
@router.get('/me', response_model=auth.ProfileOut)
def profile_route(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------------------------------------
#                SEND VERIFICATION CODE
# -------------------------------------------------------
@router.post('/send-code')
async def send_code_route(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    await send_code(current_user.email, current_user.id, db=db)
    return {'message': 'Code sent'}



# -------------------------------------------------------
#                  VERIFY EMAIL CODE
# -------------------------------------------------------
@router.post('/verify')
def verify_code_route(data: auth.EmailCodeIn, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    verify_code(code=data.code, user_id=current_user.id, db=db)
    return {"message": "Successfully verified"}



# -------------------------------------------------------
#                  UPDATE PASSWORD
# -------------------------------------------------------
@router.post('/password/update')
def password_update_route(data: auth.PasswordUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    password_update(data=data, user_id=current_user.id, db=db)
    return {"message": "Password updated"}


# -------------------------------------------------------
#                  UPDATE EMAIL
# -------------------------------------------------------
@router.post('/email/update')
def email_update_route(data: auth.EmailUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    email_update(new_email=data.email, current_user=current_user, db=db)
    return {"message": "Email updated"}


# -------------------------------------------------------
#                  UPDATE USERNAME
# -------------------------------------------------------
@router.post('/username/update')
def username_update_route(data: auth.UsernameUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    username_update(new_username=data.username, current_user=current_user, db=db)
    return {"message": "Username updated"}


# -------------------------------------------------------
#              REFRESH ACCESS TOKEN
# -------------------------------------------------------
@router.post('/refresh', response_model=auth.LoginOut)
def refresh_access_token_route(data: auth.RefreshToken, db: Session = Depends(get_db)):
    return refresh_access_token(refresh_token=data.refresh_token, db=db)



# -------------------------------------------------------
#                 FORGOT PASSWORD
# -------------------------------------------------------

# send reset code
@router.post('/reset-code')
async def send_reset_code_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    await send_reset_code(current_user=current_user, db=db)
    return {"message": "reset code sent"}


# verify and change
@router.post('/forgot-password')
def forgot_password_route(data: auth.ResetPasswordUpdateIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_reset_password(code=data.code, new_password=data.new_password, current_user=current_user, db=db)
    return {"message": "password updated"}


# -------------------------------------------------------
#                 DELETE ACCOUNT
# -------------------------------------------------------
@router.delete('/delete-account')
def delete_account_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_user(current_user=current_user, db=db)
    return {"message": "Account deleted"}
