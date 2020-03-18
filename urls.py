from django.urls import path
from . import views
from .views import new_post

urlpatterns = [
    # path('', views.post_list, name='post_list'),
    url(r'^new_post/$', new_post, name='create-post'),
]
