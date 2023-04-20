"""Custom authentication backend for Keycloak. When a user first logs in, they will be created in the django."""
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class KeycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """Custom authentication backend for Keycloak.

    When a user first logs in, they will be created in the django
    auth database via a call to create_user(). When a user logs in again, they will be updated via a call to
    update_user().
    """

    def create_user(self, claims):
        """Create a user in the django auth database when a user logs in for the first time via Keycloak."""
        user = super().create_user(claims)
        user.username = claims.get("preferred_username")
        user.save()
        return user

    def update_user(self, user, claims):
        """Update a user in the django auth database when a user logs in again via Keycloak."""
        user.username = claims.get("preferred_username")
        user.save()
        return user
