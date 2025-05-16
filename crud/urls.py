from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # login
	path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # Gender URLs
    path('genders/list', login_required(views.gender_list), name='gender_list'),
    path('genders/add', login_required(views.add_gender), name='add_gender'),
    path('genders/edit/<int:genderId>', login_required(views.edit_gender), name='edit_gender'),
    path('genders/delete/<int:genderId>', login_required(views.delete_gender), name='delete_gender'),

    # User URLs
    path('users/add', login_required(views.add_user), name='add_user'),
    path('users/list', login_required(views.user_list), name='user_list'),
    path('users/edit/<int:userId>', login_required(views.edit_user), name='edit_user'),
    path('users/delete/<int:userId>', login_required(views.delete_user), name='delete_user'),

    # search URLs
    path('users/search_users', login_required(views.search_users), name='search-users'),
    path('users/profile', login_required(views.profile_page), name='profile'),
    path('users/live-search', login_required(views.live_search), name='live-search'),
    
    path('change-password/', views.change_password, name='change_password'),



    
]

