"""Custom authentication backend for Keycloak. When a user first logs in, they will be created in the django."""
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from apps.data_tables.models import AccessAttribute, Classification


class KeycloakOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """Custom authentication backend for Keycloak.

    When a user first logs in, they will be created in the django
    auth database via a call to create_user(). When a user logs in again, they will be updated via a call to
    update_user().
    """

    def create_user(self, claims):
        """Create a user in the django auth database when a user logs in for the first time via Keycloak."""
        user = super().create_user(claims)
        self.__sync_user(user, claims)
        return user

    def update_user(self, user, claims):
        """Update a user in the django auth database when a user logs in again via Keycloak."""
        self.__sync_user(user, claims)
        return user

    def __sync_user(self, user, claims):
        """Sync a user in the django auth database from Keycloak claims."""
        user.username = claims.get("preferred_username")

        # TODO: Maybe add a shortname field to the Classification model?
        clearance_map = {
            "U": "UNCLASSIFIED",
            "C": "CONFIDENTIAL",
            "S": "SECRET",
            "TS": "TOPSECRET",
        }

        # Update the user's clearance
        clearance_shortname = claims.get("clearance")

        try:
            clearance = Classification.objects.get(name=clearance_map[clearance_shortname])
        except KeyError:
            clearance = Classification.objects.get(name="UNCLASSIFIED")
        user.clearance = clearance

        # Update the user's access attributes
        sci_list = claims.get("sci", [])
        attr_model_list = []
        for sci in sci_list:
            attribute = "sci=" + str(sci).lower()
            # Create an attribute model for each sci
            attr_model = AccessAttribute.objects.get_or_create(name=attribute)
            attr_model_list.append(attr_model[0])

        # Update the user's NTK attributes
        ntk_list = claims.get("ntk", [])
        for ntk in ntk_list:
            attribute = "ntk=" + str(ntk).lower()
            # Create an attribute model for each ntk
            attr_model = AccessAttribute.objects.get_or_create(name=attribute)
            attr_model_list.append(attr_model[0])
        
        # Update the user's Nationality attributes
        nat_list = claims.get("nationality", [])
        for nat in nat_list:
            attribute = "nationality=" + str(nat).lower()
            # Create an attribute model for each nat
            attr_model = AccessAttribute.objects.get_or_create(name=attribute)
            attr_model_list.append(attr_model[0])

        user.access_attributes.set(attr_model_list)
        user.save()
        return user
