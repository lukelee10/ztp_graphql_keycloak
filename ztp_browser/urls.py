from django.contrib import admin
from django.urls import include, path

from apps.data_tables.views import graphql_view
from apps.users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user_views.login, name="login"),
    path("logout/", user_views.LogoutView.as_view(), name="logout"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("ping/", user_views.ping, name="ping"),
    path("graphql", graphql_view, name="graphql"),
    path("", user_views.index, name="index"),
]
