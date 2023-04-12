"""Single Sign-On (SSO) with Keycloak."""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from keycloak import KeycloakOpenID
from ztpvis import settings
from ztpvis.graphql import router

# Keycloak configuration
keycloak_openid = KeycloakOpenID(
    server_url=settings.keycloak_server_url,
    client_id=settings.keycloak_client_id,
    realm_name=settings.keycloak_realm,
    client_secret_key=settings.keycloak_client_secret,
)

router = APIRouter()


async def load_userinfo(request: Request):
    """Loads the user info from Keycloak."""
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        user_info = keycloak_openid.userinfo(access_token)
        token_info = keycloak_openid.introspect(access_token)
        request.state.userinfo = user_info
        request.state.tokeninfo = token_info
    except Exception as err:
        raise HTTPException(status_code=401, detail="Not authenticated") from err


@router.get("/login")
async def login(request: Request):
    """Redirects the user to the Keycloak login page."""
    redirect_uri = request.url_for("callback")
    auth_url = keycloak_openid.auth_url(
        redirect_uri=str(redirect_uri), scope="openid profile email"
    )
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def callback(request: Request, code: str):
    """Keycloak redirects to this URL after successful authentication."""
    if code:
        redirect_uri = request.url_for("callback")
        tokens = keycloak_openid.token(
            grant_type="authorization_code", code=code, redirect_uri=str(redirect_uri)
        )
        request.session["access_token"] = tokens.get("access_token")
        request.session["refresh_token"] = tokens.get("refresh_token")
        return RedirectResponse(url="/")
    return "Something went wrong", 400


@router.get("/logout")
async def logout(request: Request):
    """Logs out the user from the application."""
    refresh_token = request.session.get("refresh_token")
    if refresh_token:
        keycloak_openid.logout(refresh_token=refresh_token)
        del request.session["refresh_token"]
        del request.session["access_token"]
    return RedirectResponse(url="/")
