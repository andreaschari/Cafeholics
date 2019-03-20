from cafe import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^cafes/$', views.cafes, name='cafes'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/$', views.chosen_cafe, name='chosen_cafe'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/edit_review/$', views.EditReviewView.as_view(), name='edit_review'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/write_review/$', views.write_review, name='write_review'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/edit_cafe/$', views.EditCafeView.as_view(), name='edit_cafe'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/delete_cafe/$', views.delete_cafe, name='delete_cafe'),
    url(r'^cafe/(?P<username>[\w\-]+)/delete_account/$', views.delete_account, name='delete_account'),
    url(r'^cafes/(?P<cafe_name_slug>[\w\-]+)/delete_review/$', views.delete_review, name='delete_review'),
    url(r'^search/$', views.search, name='search_results'),
    url(r'^register/$', views.sign_up, name='sign_up'),
    url(r'^my_account/$', views.my_account, name='my_account'),
    url(r'^cafe/edit_account/$', views.edit_account, name='edit_account'),
    url(r'^cafe/password/$', views.change_password, name='change_password'),
    url(r'^my_account/my_cafes/$', views.my_cafes, name='my_cafes'),
    url(r'^my_account/my_cafes/add_cafe/$', views.add_cafe, name='add_cafe'),
    url(r'^my_account/my_reviews/$', views.my_reviews, name='my_reviews'),
]
