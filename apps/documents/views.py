from django.contrib.auth.decorators import login_required
from strawberry.django.views import GraphQLView

from apps.documents.schema import schema


@login_required
def graphql_view(request):
    return GraphQLView.as_view(schema=schema)(request)
