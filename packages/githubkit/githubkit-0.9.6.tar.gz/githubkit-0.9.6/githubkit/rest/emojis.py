"""DO NOT EDIT THIS FILE!

This file is auto generated by github rest api description.
See https://github.com/github/rest-api-description for more information.
"""


from typing import TYPE_CHECKING, overload

from pydantic import BaseModel, parse_obj_as

from githubkit.utils import exclude_unset

from .models import EmojisGetResponse200

if TYPE_CHECKING:
    from githubkit import GitHubCore
    from githubkit.response import Response


class EmojisClient:
    def __init__(self, github: "GitHubCore"):
        self._github = github

    def get(
        self,
    ) -> "Response[EmojisGetResponse200]":
        url = "/emojis"

        return self._github.request(
            "GET",
            url,
            response_model=EmojisGetResponse200,
        )

    async def async_get(
        self,
    ) -> "Response[EmojisGetResponse200]":
        url = "/emojis"

        return await self._github.arequest(
            "GET",
            url,
            response_model=EmojisGetResponse200,
        )
