import json
from typing import List

import strawberry
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from jinja2 import Template
from starlette.middleware.sessions import SessionMiddleware
from strawberry.fastapi import GraphQLRouter

from fastapi.templating import Jinja2Templates


async def load_userinfo(request: Request):
    access_token = request.session.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        user_info = keycloak_openid.userinfo(access_token)
        token_info = keycloak_openid.introspect(access_token)
        request.state.userinfo = user_info
        request.state.tokeninfo = token_info
    except HTTPException as err:
        raise HTTPException(status_code=401, detail="Not authenticated") from err
