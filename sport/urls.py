from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/<int:profile_id>/", views.profile_id, name="profile_id"),
    path("profile/", views.profile, name="profile"),
    path("booking", views.booking, name="booking"),
    path("club/<int:club_id>", views.club_id, name="club_id"),
    path("create_club/", views.create_club, name="create_club"),
    path("error/", views.error, name="error"),
    path("field/<int:field_id>/", views.field_view, name="field_view"),
    path("create_field/<int:club_id>", views.create_field, name="create_field"),
    path("get_fields/<int:category_id>/<str:date>", views.get_fields, name="get_fields"),
    path("schedule/<int:field_id>/<str:date>", views.get_schedule, name="get_schedule"),

]

