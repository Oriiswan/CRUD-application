from django.urls import path
from . import views

urlpatterns = [
	path('genders/list', views.gender_list),
	path('genders/add', views.add_gender),
	path('genders/edit/<int:genderId>', views.edit_gender),
	path('genders/delete/<int:genderId>', views.delete_gender),
	path('users/add', views.add_user),
	path('users/list', views.user_list),
	path('users/edit/<int:userId>', views.edit_user),
	path('users/delete/<int:userId>', views.delete_user),
<<<<<<< HEAD
    path('users/login', views.login)
    
=======
	path('users/profile/<int:userId>', views.user_profile),

>>>>>>> ff2d55e993facd80c5c0fa47dfef2bb1b2e230d6
]
