from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import status
from app.v1.schema.token_schema import Token
from app.v1.service.user_service import CreateUser
from app.v1.service.auth_service import AuthService
from app.v1.service.profile_service import ProfileService
from fastapi.security import OAuth2PasswordRequestForm
from app.v1.schema.user_schema import UserRegister, User, UserProfile
from app.v1.schema.user_schema import UserLogin

router = APIRouter(prefix="/api/v1")
auth_class = AuthService()


@router.post("/user/", tags=["users"],
             status_code=status.HTTP_201_CREATED,
             response_model=User,
             summary="Create a new user")
def create_user(user: UserRegister = Body(...)):
    """
    ## Create a new user in the app

    ### Args
    The app can recive next fields into a JSON
    - email: A valid email
    - username: Unique username
    - password: Strong password for authentication
    ### Returns
    - user: User info
    """
    UserClass = CreateUser()
    return UserClass.register_user(user)


@router.post("/user/login_web/", tags=["users"], response_model=Token)
def login_for_web(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    ## Login for web
    ### Args
    The app can recive next fields into a JSON
    - username: Unique username
    - password: Strong password for authentication
    ### Returns
    - token: Token for authentication
    """

    access_token = auth_class.generate_token(form_data.username,
                                             form_data.password)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/user/login/", tags=["users"], response_model=Token)
async def login_for_access_token(user: UserLogin = Body(...)):
    """
    ## Login for access token

    ### Args
    The app can receive next fields by json data
    - username: Your username or email
    - password: Your password

    ### Returns
    - access token and token type
    """
    access_token = auth_class.generate_token(user.username, user.password)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/user/profile/", tags=["profiles"], response_model=UserProfile)
def get_user_profile(current_user:
                     User = Depends(auth_class.get_current_user)):
    """
    ## Get user profile

    ### Args
    The app cant receive arguments
    but need a valid token session

    ### Returns
    - user profile
    """
    ProfileClass = ProfileService()
    return ProfileClass.get_user_profile(current_user.user_id)
