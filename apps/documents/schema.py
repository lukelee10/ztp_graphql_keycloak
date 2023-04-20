from typing import List

import strawberry.django
from django.db.models import Q

from apps.documents.models import Classification as ClassificationModel
from apps.documents.models import Document as DocumentModel
from apps.documents.types import Classification, Document, Portion
from apps.users.types import User

__CLEARANCE_LEVELS = []


def clearance_levels():
    """Create a list of clearance levels based on the classifications in the database.

    Order is important here. The index of each clearance level in the list will be used to determine the user's clearance level.
    """
    global __CLEARANCE_LEVELS
    if not __CLEARANCE_LEVELS:
        __CLEARANCE_LEVELS = [
            None,
            ClassificationModel.objects.get_or_create(name="UNCLASSIFIED")[0],
            ClassificationModel.objects.get_or_create(name="CONFIDENTIAL")[0],
            ClassificationModel.objects.get_or_create(name="SECRET")[0],
            ClassificationModel.objects.get_or_create(name="TOPSECRET")[0],
        ]
    return __CLEARANCE_LEVELS


@strawberry.type
class Query:
    documents: List[Document] = strawberry.django.field()
    portions: List[Portion] = strawberry.django.field()
    classifications: List[Classification] = strawberry.django.field()

    @strawberry.field
    def current_user(self, info) -> User:
        return info.context.request.user

    @strawberry.field
    def search(self, info, query: str) -> List[Document]:
        """Search for documents by title or content. Users will only see documents they have access to based on their clearance and the document's classification."""
        user = info.context.request.user

        # Filter documents by title or content
        documents = DocumentModel.objects.filter(Q(title__icontains=query) | Q(portions__content__icontains=query))

        # Create a list of allowed clearance levels based on the user's clearance
        allowed_clearance_levels = clearance_levels()[: clearance_levels().index(user.clearance) + 1]

        # Filter documents based on user clearance
        return documents.filter(classification__in=allowed_clearance_levels)


schema = strawberry.Schema(query=Query)
