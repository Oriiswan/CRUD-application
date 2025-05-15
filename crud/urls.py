from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.login, name='login'),
    
    # Gender URLs
    path('genders/list', views.gender_list, name='gender_list'),
    path('genders/add', views.add_gender, name='add_gender'),
    path('genders/edit/<int:genderId>', views.edit_gender, name='edit_gender'),
    path('genders/delete/<int:genderId>', views.delete_gender, name='delete_gender'),
    
    # User URLs
    path('users/add', views.add_user, name='add_user'),
    path('users/list', views.user_list, name='user_list'),
    path('users/edit/<int:userId>', views.edit_user, name='edit_user'),
    path('users/delete/<int:userId>', views.delete_user, name='delete_user'),
	
    # search URLs
    path('users/search_users', views.search_users, name='search-users'),
    path('users/live-search', views.live_search, name='live-search'),

]
