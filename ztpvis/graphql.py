from typing import List
from fastapi import Request

import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from ztpvis.database import pool


# Maps user's roles to a clearance
ROLE_TO_CLEARANCE_MAP = {
    "clearance_top_secret": "TOPSECRET",
    "clearance_confidential": "CONFIDENTIAL",
    "clearance_secret": "SECRET",
    "clearance_unclassified": "UNCLASSIFIED",
}


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

    def roles_to_classifications(self) -> List[str]:
        """Function to convert roles to classifications"""
        return [ROLE_TO_CLEARANCE_MAP[role] for role in self.roles]


@strawberry.type
class Portion:
    id: int
    document_id: int
    text: str
    classification: str
    created_at: str


@strawberry.type
class Document:
    id: int
    title: str
    classification: str
    created_at: str
    # portions: List[Portion]

    # Define a resolver for the portions field
    @strawberry.field
    def portions(self, info: Info) -> List[Portion]:
        user: User = info.context.get("user")
        if user is None:
            # If no user is logged in, return an empty list
            return []

        user_classifications = user.roles_to_classifications()

        with pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, document_id, text, classification, created_at FROM portion WHERE document_id = %s",
                    (self.id,),
                )
                result = cursor.fetchall()
                portions = [
                    Portion(
                        id=row[0],
                        document_id=row[1],
                        text=row[2],
                        classification=row[3],
                        created_at=row[4],
                    )
                    for row in result
                    if row[3] in user_classifications  # or row[3] == "UNCLASSIFIED"
                ]
                cursor.close()
            pool.putconn(conn)
        return portions


@strawberry.type
class Query:
    @strawberry.field
    def documents(self, info: Info) -> List[Document]:
        with pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, title, classification, created_at FROM document"
                )
                result = cursor.fetchall()
                documents = [
                    Document(
                        id=row[0],
                        title=row[1],
                        classification=row[2],
                        created_at=row[3],
                    )
                    for row in result
                ]
                cursor.close()
            pool.putconn(conn)
        return documents

    @strawberry.field
    def records(self, info: Info) -> List[Record]:
        user = info.context.get("user")

        if user is not None and user.roles:
            user_classifications = user.roles_to_classifications()
            with pool.getconn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM records WHERE clearance IN %s",
                        (tuple(user_classifications),),
                    )
                    rows = cursor.fetchall()
                    cursor.close()
                pool.putconn(conn)
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
