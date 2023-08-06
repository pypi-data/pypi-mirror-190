from http import HTTPStatus
from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    serial_number: str,
    *,
    client: AuthenticatedClient,
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    resolution: Union[Unset, None, str] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/devices/{serialNumber}/samples".format(
        client.base_url, serialNumber=serial_number
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["start"] = start

    params["end"] = end

    params["pageSize"] = page_size

    params["resolution"] = resolution

    params["cursor"] = cursor

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
    serial_number: str,
    *,
    client: AuthenticatedClient,
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    resolution: Union[Unset, None, str] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get Samples belonging to a specific Device (latest segment)

    Args:
        serial_number (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        page_size (Union[Unset, None, int]):
        resolution (Union[Unset, None, str]):
        cursor (Union[Unset, None, str]):
        organization_id (Union[Unset, None, str]):
        user_group_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        serial_number=serial_number,
        client=client,
        start=start,
        end=end,
        page_size=page_size,
        resolution=resolution,
        cursor=cursor,
        organization_id=organization_id,
        user_group_id=user_group_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    serial_number: str,
    *,
    client: AuthenticatedClient,
    start: Union[Unset, None, str] = UNSET,
    end: Union[Unset, None, str] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    resolution: Union[Unset, None, str] = UNSET,
    cursor: Union[Unset, None, str] = UNSET,
    organization_id: Union[Unset, None, str] = UNSET,
    user_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Get Samples belonging to a specific Device (latest segment)

    Args:
        serial_number (str):
        start (Union[Unset, None, str]):
        end (Union[Unset, None, str]):
        page_size (Union[Unset, None, int]):
        resolution (Union[Unset, None, str]):
        cursor (Union[Unset, None, str]):
        organization_id (Union[Unset, None, str]):
        user_group_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        serial_number=serial_number,
        client=client,
        start=start,
        end=end,
        page_size=page_size,
        resolution=resolution,
        cursor=cursor,
        organization_id=organization_id,
        user_group_id=user_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
