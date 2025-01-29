"""Views module."""

from flask import request, render_template
from injector import inject

from services import UserService


def index(user_service: UserService = inject(UserService) ):
    query = request.args.get("query", "Dependency Injector")
    limit = request.args.get("limit", 10, int)

    repositories = []
    users = user_service.get_all_users()

    return render_template(
        "index.html",
        query=query,
        limit=limit,
        repositories=repositories,
        users=users
    )