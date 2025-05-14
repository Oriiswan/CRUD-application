from django.urls import path
from . import views

urlpatterns = [
    path('gender/add', views.addGender),
    path('gender/list', views.genderList),
    path('user/addUser', views.addUser),
    path('gender/editGender/<int:genderId>', views.editGender),
    path('gender/deleteGender/<int:genderId>', views.deleteGender),
    path('user/userlist', views.userList),
    
]
