from fastapi import APIRouter, HTTPException
from app.models.user import UserRegister, UserLogin, ChangePasswordRequest, ChangeUsernameRequest, ForgotPasswordRequest, ResetPasswordRequest, logout
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/health")
async def health_check():
    return {"status": "OK"}


@router.post("/register")
async def register_user(user: UserRegister):
    return await user_service.register_user(user.dict())


@router.post("/login")
async def login_user(login: UserLogin):
    user = await user_service.validate_login(login.username, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login success", "user": login.username}


@router.post("/change-password")
async def change_password(change: ChangePasswordRequest):
    # Replace this with actual user extracted from JWT in production
    username = "validuser@example.com"
    return await user_service.update_password(username, change.old_password, change.new_password)


@router.post("/change-email-phone")
async def change_username(change_req: ChangeUsernameRequest):
    username = "validuser@example.com"
    try:
        return await user_service.update_email_or_phone(username, change_req.new_username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    try:
        return await user_service.handle_forgot_password(req.username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    try:
        return await user_service.handle_reset_password(req.token, req.new_password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/logout")
async def logout_user(logout: logout):
    user = await user_service.logout_user(logout.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Logout success", "user": logout.username}

