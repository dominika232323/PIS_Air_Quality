from django.urls import path
from . import views

urlpatterns = [
    path("", views.gios, name='gios')
]