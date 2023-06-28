import logging

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import utils.utils_request
from nav_manage import views_admin

logger = logging.getLogger(__name__)


def navi_list_page(request):
    resp, success = views_admin.query_admin(request)
    if not success:
        reason = resp
        return JsonResponse(data={'result': '[请求失败]', 'reason': reason})
    admin = resp
    assert isinstance(admin, views_admin.Admin)

    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    data, ok = client.list_navi()
    if not ok:
        reason = data
        logger.error("wrong reason={}".format(reason))
        return HttpResponse('[查询失败] reason={}'.format(reason))
    items = data.get('items')
    assert isinstance(items, list)
    return render(request, 'nav_manage/navi_list.html', locals())


def create_navi_page(request):
    parent_name = request.GET.get("parent_name", "")
    parent_nvid = request.GET.get("parent_nvid", 0)
    return render(request, 'nav_manage/navi_create.html', locals())


def create_navi_submit_page(request):
    if request.method == "POST":
        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.create_navi(
            name=str(request.POST.get('name')),
            parent_nvid=int(request.POST.get('parent_nvid', 0))
        )
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[添加失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        return HttpResponse('[添加失败]')


def delete_navi_page(request):
    if not request.GET.get("force"):
        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.delete_navi(
            name=str(request.GET.get('name')),
            force=False,
        )
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[删除失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        name = request.GET.get("name")
        return render(request, 'nav_manage/navi_delete.html', locals())


def delete_navi_submit_page(request):
    if request.method == "POST":
        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.delete_navi(
            name=str(request.POST.get('name')),
            force=bool(request.POST.get('force', False)),
        )
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[删除失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        return HttpResponse('[删除失败]')


def sort_navi_page(request):
    parent_nvid = int(request.GET.get("parent_nvid", 0))
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    data, status_code = client.get_navi_orders(parent_nvid=parent_nvid)
    assert status_code is 200
    navis = data.get('navis')
    assert isinstance(navis, list)
    return render(request, 'nav_manage/navi_sort.html', locals())


def sort_navi_submit_page(request):
    if request.method == 'POST':
        items = []  # "items":[{"name":"龙虎精二","sort":3}, {"name":"有凤来一","sort":2}]
        for key, value in request.POST.items():
            if key.startswith('navi_name_'):
                name = key.split('[', 1)[1][:-1]
                sort = int(value)
                items.append({"name": name, "sort": sort})
        logger.debug("sort input items={}".format(items))
        assert len(items) > 0

        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.sort_navi(items=items)
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[排序失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        return HttpResponse('[排序失败]')


def create_navi_lvl2_page(request):
    navi_name = request.GET.get("navi_name")
    return render(request, 'nav_manage/navi_create_lvl2.html', locals())


def create_navi_lvl2_submit_page(request):
    if request.method == "POST":
        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.create_navi_lvl2(
            navi_name=str(request.POST.get('navi_name')),
            name=str(request.POST.get('name')),
            text=str(request.POST.get('text')),
            link=str(request.POST.get('link')),
            is_escrow=bool(request.POST.get('is_escrow', False)),
        )
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[添加失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        return HttpResponse('[添加失败]')


def delete_navi_lvl2_page(request):
    navi_name = request.GET.get("navi_name")
    assert isinstance(navi_name, str)
    name = request.GET.get("name")
    assert isinstance(name, str)
    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    data, status_code = client.delete_navi_lvl2(navi_name=navi_name, name=name)
    if status_code != 200:
        reason = data
        logger.error("wrong reason={}".format(reason))
        return HttpResponse('[删除失败] reason={}'.format(reason))
    return navi_list_page(request)


def sort_navi_lvl2_page(request):
    navi_name = request.GET.get("navi_name")
    assert isinstance(navi_name, str)

    admin_manage_token = request.COOKIES.get("admin_manage_token")
    client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
    data, status_code = client.list_navi_lvl2(navi_name=navi_name)
    assert status_code is 200
    items = data.get('items')
    assert isinstance(items, list)
    return render(request, 'nav_manage/navi_sort_lvl2.html', locals())


def sort_navi_lvl2_submit_page(request):
    if request.method == 'POST':
        navi_name = request.POST.get("navi_name")
        assert isinstance(navi_name, str)
        items = []  # "items": [{"name": "天公", "sort": 3}, {"name": "天公2", "sort": 2}]
        for key, value in request.POST.items():
            if key.startswith('navi_lvl2_name_'):
                name = key.split('[', 1)[1][:-1]
                sort = int(value)
                items.append({"name": name, "sort": sort})
        logger.debug("sort input navi_name={} items={}".format(navi_name, items))
        assert len(items) > 0

        admin_manage_token = request.COOKIES.get("admin_manage_token")
        client = utils.utils_request.Client(prefix=settings.BACKEND_API_PREFIX, token=admin_manage_token)
        data, status_code = client.sort_navi_lvl2(navi_name=navi_name, items=items)
        if status_code != 200:
            logger.warning("status_code={} != 200".format(status_code))
            return HttpResponse('[排序失败] reason={}'.format(data))
        return navi_list_page(request)
    else:
        return HttpResponse('[排序失败]')
