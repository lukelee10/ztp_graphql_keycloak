import json

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from ztpvis import settings
from ztpvis.api import sso
from ztpvis.api.sso import load_userinfo
from ztpvis.graphql import router

app = FastAPI()
app.include_router(sso.router)
app.add_middleware(SessionMiddleware, secret_key=settings.fastapi_secret_key)
templates = Jinja2Templates(directory="templates")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    if exc.status_code == 401:
        return RedirectResponse(url="/login")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if request.session.get("access_token") is not None:
        await load_userinfo(request)
        return templates.TemplateResponse(
            "index.html.j2",
            {
                "request": request,
                "username": request.state.userinfo.get("preferred_username"),
            },
        )
    return "You are not authenticated.<br><button><a href='/login'>Login</a></button>"


@app.get("/hello", response_class=HTMLResponse, dependencies=[Depends(load_userinfo)])
async def hello(request: Request):
    username = request.state.userinfo.get("preferred_username")
    return templates.TemplateResponse(
        "hello.html.j2",
        {
            "request": request,
            "username": username,
            "token_info": json.dumps(request.state.tokeninfo, indent=2),
        },
    )


# Add GraphQL app to FastAPI but require authentication
app.include_router(
    router,
    prefix="/graphql",
    dependencies=[Depends(load_userinfo)],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
