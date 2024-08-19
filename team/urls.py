from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.accounts, name="account"),
    path("login/", views.signin, name="signin"),
    path("logout/", views.signout, name="signout"),

    path("delete_match/<str:pk>/", views.deleteMatch, name='delete_match')
]
