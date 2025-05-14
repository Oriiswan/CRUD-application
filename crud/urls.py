from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),

	path('genders/list', views.gender_list),
	path('genders/add', views.add_gender),
	path('genders/edit/<int:genderId>', views.edit_gender),
	path('genders/delete/<int:genderId>', views.delete_gender),
	path('users/add', views.add_user),
	path('users/list', views.user_list),
	path('users/edit/<int:userId>', views.edit_user),
	path('users/delete/<int:userId>', views.delete_user),

]
