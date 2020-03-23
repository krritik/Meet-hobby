from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.index,name='index'),
    path('showgroup/', views.show_joined_group, name='show_joined_group'),
    path('newgroup/', views.show_new_group, name='show_new_group'),
    path('newgroup/<int:id>', views.join_group, name='join_group'),
    path('group_posts/<int:id>',views.show_posts, name='show_posts'),
    path('new_post/<int:id>',views.new_post,name='post_new'),
    path('post_comments/<int:id>',views.show_comments, name='show_comments'),
    path('new_comment/<int:id>',views.new_comment,name='comment_new')
]
