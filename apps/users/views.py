from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mozilla_django_oidc.views import OIDCLogoutView
from strawberry.django.views import GraphQLView

from apps.data_tables.schema import schema


@login_required
@csrf_exempt
def graphql_view(request):
    return GraphQLView.as_view(schema=schema)(request)


@login_required
@csrf_exempt
def ping(request: HttpRequest):
    return JsonResponse({"message": request.user.username})


def index(request):
    return render(
        request,
        "index.html",
        {
            "user": request.user,
        },
    )


def login(request):
    return HttpResponseRedirect("/oidc/authenticate/")


def keycloak_logout_endpoint(request):
    logout_endpoint = settings.OIDC_OP_LOGOUT_ENDPOINT
    return logout_endpoint + "?redirect_uri=" + request.build_absolute_uri(settings.LOGOUT_REDIRECT_URL)


class LogoutView(OIDCLogoutView):
    """Logout view that redirects to the Keycloak logout endpoint."""

    def get(self, request):
        return self.post(request)

    def post(self, request):
        super().post(request)
        return HttpResponseRedirect(keycloak_logout_endpoint(request))
