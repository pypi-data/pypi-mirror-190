"""DO NOT EDIT THIS FILE!

This file is auto generated by github rest api description.
See https://github.com/github/rest-api-description for more information.
"""


from datetime import datetime
from typing import TYPE_CHECKING, List, Union, overload

from pydantic import BaseModel, parse_obj_as

from githubkit.utils import UNSET, Unset, exclude_unset

from .models import (
    Snapshot,
    BasicError,
    DependencyGraphDiffItems,
    ReposOwnerRepoDependencyGraphSnapshotsPostResponse201,
)
from .types import (
    MetadataType,
    SnapshotType,
    SnapshotPropJobType,
    SnapshotPropDetectorType,
    SnapshotPropManifestsType,
)

if TYPE_CHECKING:
    from githubkit import GitHubCore
    from githubkit.response import Response


class DependencyGraphClient:
    def __init__(self, github: "GitHubCore"):
        self._github = github

    def diff_range(
        self,
        owner: str,
        repo: str,
        basehead: str,
        name: Union[Unset, str] = UNSET,
    ) -> "Response[List[DependencyGraphDiffItems]]":
        url = f"/repos/{owner}/{repo}/dependency-graph/compare/{basehead}"

        params = {
            "name": name,
        }

        return self._github.request(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[DependencyGraphDiffItems],
            error_models={
                "404": BasicError,
                "403": BasicError,
            },
        )

    async def async_diff_range(
        self,
        owner: str,
        repo: str,
        basehead: str,
        name: Union[Unset, str] = UNSET,
    ) -> "Response[List[DependencyGraphDiffItems]]":
        url = f"/repos/{owner}/{repo}/dependency-graph/compare/{basehead}"

        params = {
            "name": name,
        }

        return await self._github.arequest(
            "GET",
            url,
            params=exclude_unset(params),
            response_model=List[DependencyGraphDiffItems],
            error_models={
                "404": BasicError,
                "403": BasicError,
            },
        )

    @overload
    def create_repository_snapshot(
        self, owner: str, repo: str, *, data: SnapshotType
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        ...

    @overload
    def create_repository_snapshot(
        self,
        owner: str,
        repo: str,
        *,
        data: Unset = UNSET,
        version: int,
        job: SnapshotPropJobType,
        sha: str,
        ref: str,
        detector: SnapshotPropDetectorType,
        metadata: Union[Unset, MetadataType] = UNSET,
        manifests: Union[Unset, SnapshotPropManifestsType] = UNSET,
        scanned: datetime,
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        ...

    def create_repository_snapshot(
        self,
        owner: str,
        repo: str,
        *,
        data: Union[Unset, SnapshotType] = UNSET,
        **kwargs,
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        url = f"/repos/{owner}/{repo}/dependency-graph/snapshots"

        if not kwargs:
            kwargs = UNSET

        json = kwargs if data is UNSET else data
        json = parse_obj_as(Snapshot, json)
        json = json.dict(by_alias=True) if isinstance(json, BaseModel) else json

        return self._github.request(
            "POST",
            url,
            json=exclude_unset(json),
            response_model=ReposOwnerRepoDependencyGraphSnapshotsPostResponse201,
        )

    @overload
    async def async_create_repository_snapshot(
        self, owner: str, repo: str, *, data: SnapshotType
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        ...

    @overload
    async def async_create_repository_snapshot(
        self,
        owner: str,
        repo: str,
        *,
        data: Unset = UNSET,
        version: int,
        job: SnapshotPropJobType,
        sha: str,
        ref: str,
        detector: SnapshotPropDetectorType,
        metadata: Union[Unset, MetadataType] = UNSET,
        manifests: Union[Unset, SnapshotPropManifestsType] = UNSET,
        scanned: datetime,
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        ...

    async def async_create_repository_snapshot(
        self,
        owner: str,
        repo: str,
        *,
        data: Union[Unset, SnapshotType] = UNSET,
        **kwargs,
    ) -> "Response[ReposOwnerRepoDependencyGraphSnapshotsPostResponse201]":
        url = f"/repos/{owner}/{repo}/dependency-graph/snapshots"

        if not kwargs:
            kwargs = UNSET

        json = kwargs if data is UNSET else data
        json = parse_obj_as(Snapshot, json)
        json = json.dict(by_alias=True) if isinstance(json, BaseModel) else json

        return await self._github.arequest(
            "POST",
            url,
            json=exclude_unset(json),
            response_model=ReposOwnerRepoDependencyGraphSnapshotsPostResponse201,
        )
