from django.urls import path

from . import views

app_name = 'ira'
urlpatterns = [
    path("", views.index, name="index"),
]
