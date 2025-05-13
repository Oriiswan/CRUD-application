from django.urls import path
from . import views

urlpatterns = [
    path('gender/add', views.addGender),
    path('gender/list', views.genderList),
    path('gender/addUser', views.addUser)
]
