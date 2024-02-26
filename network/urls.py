
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<int:user_id>", views.user_profile_view, name="user_profile"),
    path("following",views.following_views, name="following"),
    #API:
    path("edit_post/<int:post_id>",views.edit_post_views, name="edit_post"),
    path("likes_change",views.likes_change_API_views, name="likes_change_API_views")
]
