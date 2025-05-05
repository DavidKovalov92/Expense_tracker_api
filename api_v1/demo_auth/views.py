import secrets
import stat
from time import time
from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core import security

router = APIRouter(prefix="/demo-auth", tags=["Demo auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


username_and_password = {
    "admin": "admin",
}


def get_auth_user_username(
    credentials: HTTPBasicCredentials = Depends(security),
):
    unauth_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_and_password.get(credentials.username)
    if correct_password is None:
        raise unauth_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauth_exc
    return credentials.username


@router.get("/basic-auth-username")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}",
        "username": auth_username,
    }


static_auth_token_and_username = {
    "f6d7c026b7a1648ebe2033e062c0": "admin",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
):

    if username := static_auth_token_and_username.get(static_token):
        return username

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect token",
    )


@router.get("/http-header-auth")
def demo_auth_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}",
        "username": username,
    }


COOKIES = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect token",
        )
    return COOKIES[session_id]


@router.post("/login-cookie")
def demo_auth_login_set_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {"username": auth_username, "login_at": int(time())}
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/check-cookie")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hi, {username}",
        **user_session_data,
    }


@router.get("/logout-cookie")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}",
    }
