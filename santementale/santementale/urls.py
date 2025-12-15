from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from mood import views 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mood.urls")),      
    path('', lambda request: redirect('connexion'))       
]
