from django.conf.urls import url
from .views import *



urlpatterns=[
    url(r'^login/$', login_views),
    url(r'^register/$', register_views),
    url(r'^checkphone/$',checkphone_views),
    url(r'^$', index_views),
    url(r'^all_type_goods/$',all_type_goods_views),
    url(r'^check_login/$', check_login_views),
    url(r'^logout/$',logout_views),
    url(r'^add_cart/$',add_cart_views),
    url(r'^dict/$',dict_views),


]
