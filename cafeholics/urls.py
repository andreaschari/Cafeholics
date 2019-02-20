"""cafeholics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cafeholics import views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),

    url(r'^cafes/$', views.cafes, name='cafes'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/$', views.chosen_cafe, name='chosen_cafe'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/edit_review/$', views.edit_review, name='edit_review'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/write_review/$', views.write_review, name='write_review'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/edit_cafe/$', views.edit_cafe, name='edit_cafe'),

    url(r'^search_results/', views.search_results, name='search_results'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^login/my_account/$', views.my_account, name='my_account'),
    url(r'^login/my_account/my_cafes/$', views.my_cafes, name='my_cafes'),
    url(r'^login/my_account/my_cafes/add_cafe/$', views.add_cafe, name='add_cafe'),
    url(r'^login/my_account/my_reviews/$', views.my_reviews, name='my_reviews'),
    url(r'^logout/$', views.user_logout, name='logout'),
]
