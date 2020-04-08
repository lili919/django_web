from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'', views.blog_list, name = 'blog_list'),
]