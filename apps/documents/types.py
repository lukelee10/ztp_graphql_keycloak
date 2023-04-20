from typing import List

import strawberry.django
from strawberry import auto

from apps.documents import models


@strawberry.django.type(models.Classification)
class Classification:
    id: auto
    name: auto
    created_at: auto
    updated_at: auto


@strawberry.django.type(models.Document)
class Document:
    id: auto
    title: auto
    classification: Classification
    created_at: auto
    updated_at: auto
    portions: List["Portion"] = strawberry.django.field()


@strawberry.django.type(models.Portion)
class Portion:
    id: auto
    document: Document
    classification: Classification
    content: auto
    created_at: auto
    updated_at: auto
