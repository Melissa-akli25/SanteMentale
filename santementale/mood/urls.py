from django.urls import path
from . import views

urlpatterns = [
    path("connexion/", views.connexion, name="connexion"),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("articles/", views.articles, name="articles"),
    path("exercices/", views.exercices, name="exercices"),
    path("numeros/", views.numeros, name="numeros"),
    path("profile/", views.profile, name="profile"),
    path("resolutions/", views.resolutions, name="resolutions"),
    path("tracking/", views.tracking, name="tracking"),
    path("changeinfos/", views.change_infos, name="changeinfos"),
    path("changemdp/", views.change_mdp, name="changemdp"),
    path("savetracking/", views.save_tracking, name="save_tracking"),
    path("saveresolution/", views.save_resolution, name="save_resolution"),
    path("resolutions/toggle/<int:id>/", views.toggle_resolution, name="toggle_resolution"),
    path("resolutions/delete/<int:id>/", views.delete_resolution, name="delete_resolution"),


]
