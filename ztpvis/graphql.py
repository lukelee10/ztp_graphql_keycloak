from typing import List
from fastapi import Request

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from ztpvis.database import pool


@strawberry.type
class Record:
    """Record type for GraphQL"""

    id: int
    data: str
    clearance: str


@strawberry.type
class User:
    """User type for GraphQL"""

    username: str
    email: str
    preferred_username: str
    email_verified: bool
    active: bool
    roles: List[str]


# define GraphQL resolvers
@strawberry.type
class Query:
    @strawberry.field
    def records(self, info: Info) -> List[Record]:
        user = info.context.get("user")

        # Maps user's roles to a record's clearance
        clearance_mapping = {
            "clearance_top_secret": "TOPSECRET",
            "clearance_confidential": "CONFIDENTIAL",
            "clearance_secret": "SECRET",
            "clearance_unclassified": "UNCLASSIFIED",
        }

        if user is not None and user.roles:
            user_clearances = [clearance_mapping.get(role) for role in user.roles]
            with pool.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM records WHERE clearance IN %s",
                        (tuple(user_clearances),),
                    )
                    rows = cursor.fetchall()
        else:
            # Deny everything, return nothing (perhaps this should be an error instead?)
            return []
        return [Record(**dict(zip(["id", "data", "clearance"], row))) for row in rows]

    @strawberry.field
    def current_user(self, info: Info) -> User:
        return info.context.get("user")


async def get_context(request: Request):
    token_info = request.state.tokeninfo
    return {
        "user": User(
            username=token_info["username"],
            email=token_info["email"],
            preferred_username=token_info["preferred_username"],
            email_verified=token_info["email_verified"],
            active=token_info["active"],
            roles=token_info.get("realm_access", {}).get("roles", []),
        )
    }


schema = strawberry.Schema(query=Query)
router = GraphQLRouter(
    schema=schema,
    context_getter=get_context,
    graphiql=True,
)
