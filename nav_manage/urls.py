from django.urls import path

from . import views, views_navis

urlpatterns = [
    path("", views.index, name="index"),
    path('admin_login', views.admin_login_page, name='admin_login_page'),
    path('admin_login/submit', views.admin_login_submit_page, name='admin_login_submit_page'),
    path('admin_logout', views.admin_logout_page, name='admin_logout_page'),
    path('admin_logout/submit', views.admin_logout_submit_page, name='admin_logout_submit_page'),
    path('create_admin', views.create_admin_page, name='create_admin_page'),
    path('create_admin/submit', views.create_admin_submit_page, name='create_admin_submit_page'),
    path('admin_information', views.admin_information_page, name='admin_information_page'),
    path('unimplemented_msg', views.unimplemented_msg_page, name='unimplemented_msg_page'),
    path('admin_list', views.admin_list_page, name='admin_list_page'),
    path('admin_of_mine_list', views.admin_of_mine_list_page, name='admin_of_mine_list_page'),

    # 我单独把导航页面相关的放到一个文件里，接口也聚集在这一块
    path('navi_list', views_navis.navi_list_page, name='navi_list_page'),
    path('create_navi', views_navis.create_navi_page, name='create_navi_page'),
    path('create_navi/submit', views_navis.create_navi_submit_page, name='create_navi_submit_page'),
    path('delete_navi', views_navis.delete_navi_page, name='delete_navi_page'),
    path('delete_navi/submit', views_navis.delete_navi_submit_page, name='delete_navi_submit_page'),
    path('sort_navi', views_navis.sort_navi_page, name='sort_navi_page'),
    path('sort_navi/submit', views_navis.sort_navi_submit_page, name='sort_navi_submit_page'),

    path('create_navi_lvl2', views_navis.create_navi_lvl2_page, name='create_navi_lvl2_page'),
    path('create_navi_lvl2/submit', views_navis.create_navi_lvl2_submit_page, name='create_navi_lvl2_submit_page'),
    path('delete_navi_lvl2', views_navis.delete_navi_lvl2_page, name='delete_navi_lvl2_page'),
    path('sort_navi_lvl2', views_navis.sort_navi_lvl2_page, name='sort_navi_lvl2_page'),
    path('sort_navi_lvl2/submit', views_navis.sort_navi_lvl2_submit_page, name='sort_navi_lvl2_submit_page'),
]
