import logging

from django.http import JsonResponse

import utils.utils_request
from django.conf import settings

logger = logging.getLogger(__name__)


class Admin:
    def __init__(self, username: str, nickname: str, permissions: dict, created_by_uname: str):
        assert username
        self.username = username
        assert nickname
        self.nickname = nickname
        assert isinstance(permissions, dict)
        self.permissions = permissions
        self.created_by_uname = created_by_uname


def query_admin(request) -> (Admin, bool):
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    data, status_code = client.get_admin()
    if status_code != 200:
        reason = "status_code={} != 200 reason={}".format(status_code, data)
        return reason, False
    admin = parse_admin(data)
    return admin, True


def parse_admin(data):
    username = data.get('username')
    nickname = data.get('nickname')
    permissions = data.get('permissions')
    created_by_uname = data.get('createdByUname')
    logger.debug("username={} nickname={} permissions={}".format(username, nickname, permissions))
    admin = Admin(
        username=username,
        nickname=nickname,
        permissions=permissions,
        created_by_uname=created_by_uname,
    )
    return admin


def list_admin(request) -> (list[Admin], bool):
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    res, status_code = client.list_admin()
    if status_code != 200:
        reason = "status_code={} != 200 reason={}".format(status_code, res)
        return reason, False
    items = res.get('items')
    assert isinstance(items, list)
    admins = [parse_admin(data=item) for item in items]
    return admins, True


def list_admin_of_mine(request):
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    res, status_code = client.list_admin_of_mine()
    if status_code != 200:
        reason = "status_code={} != 200 reason={}".format(status_code, res)
        return reason, False
    assert isinstance(res.get('items'), list)
    items = res.get('items')
    admins = [parse_admin(data=item) for item in items]
    return admins, True
