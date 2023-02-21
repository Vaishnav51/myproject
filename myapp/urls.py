from django.urls import path
from . import views

urlpatterns = [
    path('/hi/<str:pk>', views.hi),
    path('/compare', views.compare),
    path('/hello/hi', views.home)
]


