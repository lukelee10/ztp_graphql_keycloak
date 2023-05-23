from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from apps.data_tables.schema import schema


@login_required
@csrf_exempt
def graphql_view(request):
    return GraphQLView.as_view(schema=schema)(request)
