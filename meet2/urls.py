from django.urls import path
from . import views
from .views import new_post

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.index,name='index')
    # path('', views.post_list, name='post_list'),
    url(r'^new_post/$', new_post, name='create-post'),
]
