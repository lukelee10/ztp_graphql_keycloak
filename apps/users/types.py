from typing import List

import strawberry.django
from strawberry import auto

from apps.data_tables.types import AccessAttributeType, ClassificationType
from apps.users import models


@strawberry.django.type(models.User)
class UserType:
    id: auto
    username: auto
    first_name: auto
    last_name: auto
    email: auto
    is_staff: auto
    is_active: auto
    date_joined: auto
    last_login: auto
    clearance: ClassificationType
    access_attributes: List["AccessAttributeType"] = strawberry.django.field()
