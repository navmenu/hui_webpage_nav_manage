import datetime
import uuid

from django.shortcuts import render
from django.http import HttpResponse
import logging

import utils.utils_request
from django.conf import settings
from django.http import JsonResponse

from nav_manage import views_admin

logger = logging.getLogger(__name__)


def index(request):
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    if not admin_manage_token:
        admin_manage_token = str(uuid.uuid4())
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    pong, status_code = client.ping(value="django_nav_manage")
    logger.info("ping->pong={} status={}".format(pong, status_code))
    if status_code == 200:
        resp, success = views_admin.query_admin(request)
        if not success:
            reason = resp
            return JsonResponse(data={'result': '[请求失败]', 'reason': reason})
        admin = resp
        assert isinstance(admin, views_admin.Admin)
        return render(request, 'nav_manage/index.html', locals())
    elif status_code == 401:  # 没有权限需要跳转到登陆页面
        return admin_login_page(request)
    elif status_code == 204:  # 这是个约定，当这个接口返回204的时候，表示没有管理员，跳到创建管理员页面
        return create_admin_page(request, delete_token=True)
    else:
        return HttpResponse('[其它错误] reason={}'.format(pong))


def admin_login_page(request):
    return render(request, 'nav_manage/admin_login.html', locals())


def admin_login_submit_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=settings.BACKEND_ANONYMOUS_TOKEN)
        data, status_code = client.admin_login(username=username, password=password)
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[登录失败] reason={}'.format(data))

        logger.info("data={}".format(data))
        username = data.get("username")
        assert isinstance(username, str)
        nickname = data.get("nickname")
        assert isinstance(nickname, str)
        admin_manage_token = data.get("token")
        assert isinstance(admin_manage_token, str)
        expire_at_ns = int(data.get("expireAtNs"))
        logger.info("expire_at={}".format(expire_at_ns))
        expires = datetime.datetime.fromtimestamp(expire_at_ns / 1e9)
        logger.info("expires={}".format(expires))
        if expires < datetime.datetime.now():
            raise Exception("wrong expires wrong expire_at_ns")

        response = render(request, 'nav_manage/admin_login_success.html', locals())

        response.set_cookie("username", username, expires=expires)
        response.set_cookie("nickname", data.get("nickname").encode('utf-8').decode('iso-8859-1'), expires=expires)
        response.set_cookie("admin_manage_token", admin_manage_token, expires=expires)
        return response
    else:
        return HttpResponse('[登录失败]')


def create_admin_page(request, delete_token=False):
    response = render(request, 'nav_manage/create_admin.html', locals())
    if delete_token:
        response.delete_cookie("admin_manage_token")
    return response


def create_admin_submit_page(request):
    if request.method == "POST":
        admin_manage_token = request.COOKIES.get("admin_manage_token")
        if not admin_manage_token:
            admin_manage_token = settings.BACKEND_ANONYMOUS_TOKEN
            logger.debug("admin_manage_token={}".format(admin_manage_token))
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.create_admin(
            username=str(request.POST.get('username', '')),
            password=str(request.POST.get('password', '')),
            nickname=str(request.POST.get('nickname', '')),
            can_create_admin=bool(request.POST.get('can_create_admin', False)),
            can_select_admin=bool(request.POST.get('can_select_admin', False)),
            can_edit=bool(request.POST.get('can_edit', False)),
            can_sort=bool(request.POST.get('can_sort', False)),
        )
        if status_code != 200:
            logger.error("wrong reason={}".format(data))
            return HttpResponse('[创建失败] reason={}'.format(data))
        return index(request)
    else:
        return HttpResponse('[创建失败]')


def admin_information_page(request):
    resp, success = views_admin.query_admin(request)
    if not success:
        reason = resp
        return JsonResponse(data={'result': '[请求失败]', 'reason': reason})
    admin = resp
    assert isinstance(admin, views_admin.Admin)
    return render(request, 'nav_manage/admin_information.html', locals())


# 有些功能暂时完不成的，就跳到这里
def unimplemented_msg_page(request):
    return render(request, 'nav_manage/unimplemented_msg.html', locals())


def admin_logout_page(request):
    return render(request, 'nav_manage/admin_logout.html', locals())


def admin_logout_submit_page(request):
    response = render(request, 'nav_manage/admin_logout_success.html', locals())
    response.delete_cookie("admin_manage_token")
    return response


def admin_list_page(request):
    resp, ok = views_admin.list_admin(request)
    if not ok:
        reason = resp
        logger.error("wrong reason={}".format(reason))
        return HttpResponse('[查询失败] reason={}'.format(reason))
    admins = resp
    return render(request, 'nav_manage/admin_list.html', locals())


def admin_of_mine_list_page(request):
    resp, ok = views_admin.list_admin_of_mine(request)
    if not ok:
        reason = resp
        logger.error("wrong reason={}".format(reason))
        return HttpResponse('[查询失败] reason={}'.format(reason))
    admins = resp
    return render(request, 'nav_manage/admin_list.html', locals())
