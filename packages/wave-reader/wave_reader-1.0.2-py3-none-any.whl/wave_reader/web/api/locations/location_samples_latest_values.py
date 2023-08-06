from http import HTTPStatus
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    location_id: str,
    *,
    client: AuthenticatedClient,
    show_inactive: Union[Unset, None, bool] = False,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/locations/{locationId}/latest-samples".format(
        client.base_url, locationId=location_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["showInactive"] = show_inactive

    params["organizationId"] = organization_id

    params["userGroupId"] = user_group_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    location_id: str,
    *,
    client: AuthenticatedClient,
    show_inactive: Union[Unset, None, bool] = False,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get latest Samples belonging to devices in a specific location (latest segment)

    Args:
        location_id (str):
        show_inactive (Union[Unset, None, bool]):
        organization_id (Union[Unset, None, str]):
        user_group_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        location_id=location_id,
        client=client,
        show_inactive=show_inactive,
        organization_id=organization_id,
        user_group_id=user_group_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    location_id: str,
    *,
    client: AuthenticatedClient,
    show_inactive: Union[Unset, None, bool] = False,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get latest Samples belonging to devices in a specific location (latest segment)

    Args:
        location_id (str):
        show_inactive (Union[Unset, None, bool]):
        organization_id (Union[Unset, None, str]):
        user_group_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        location_id=location_id,
        client=client,
        show_inactive=show_inactive,
        organization_id=organization_id,
        user_group_id=user_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
