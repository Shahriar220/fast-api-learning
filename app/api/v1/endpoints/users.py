from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse, summary="Get current logged-in user profile")
def read_user_me(current_user: User = Depends(get_current_user)):
    """Protected route: Returns the profile of the user whose JWT token was sent."""
    return current_user