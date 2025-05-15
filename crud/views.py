from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core import serializers

import json


# Create your views here.
currentUsername = ''
currentPassword = ''


def gender_list(request):
    try:
        genders = Genders.objects.all()

        data = {
            'genders':genders
        }

        return render(request, 'gender/genderList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load genders: {e}')


def add_gender(request):
    try:
        if request.method == 'POST':
            gender = request.POST.get('gender')

            Genders.objects.create(gender=gender).save()
            messages.success(request, 'Gender added successfully!')
            return redirect('/genders/list')
        else:
            return render(request, 'gender/addGender.html')
    except Exception as e:
        return HttpResponse(f'Error occured during add gender: {e}')


def edit_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)

            # name of input is 'gender'
            gender = request.POST.get('gender')

            genderObj.gender = gender
            genderObj.save()

            messages.success(request, 'Gender updated successfully!')
            # gabalik sa iban nga link
            return redirect('/genders/list')

        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }


            return render(request, 'gender/editGender.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error occured during edit gender: {e}')


def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            genderObj = Genders.objects.get(pk=genderId)
            genderObj.delete()

            messages.success(request, 'Gender deleted successfully!')
            return redirect('/genders/list')

        else:
            genderObj = Genders.objects.get(pk=genderId)

            data = {
                'gender': genderObj
            }


            return render(request, 'gender/deleteGender.html', data)
    
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')


def user_list(request):
    try:

        # pagination
        p = Paginator(Users.objects.select_related('gender'), 10)
        page = request.GET.get('page')
        users = p.get_page(page)
        user_count = Users.objects.count()


        data = {
         'users': users,
         'password': currentPassword,
         'username': currentUsername,
         'user_count': user_count
    
           
        }

        return render(request, 'user/userList.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during load gender: {e}')


def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')

            form_data = {
                'fullName': request.POST.get('full_name'),
                'gender': request.POST.get('gender'),
                'birthDate': request.POST.get('birth_date'),
                'address': request.POST.get('address'),
                'contactNumber': request.POST.get('contact_number'),
                'email': request.POST.get('email'),
                'username': request.POST.get('username'),
            }

            genderObj = Genders.objects.all()

            # if username already in db:

            if Users.objects.filter(username=username).exists():

                data = {
                    'genders': genderObj,
                    'form_data': form_data,
                    'username_error': True
                }

                return render(request, 'user/addUser.html', data)

            Users.objects.create(
                full_name = fullName,
                gender = Genders.objects.get(pk=gender),
                birth_date = birthDate,
                address = address,
                contact_number = contactNumber,
                email = email,
                username = username,
                password =make_password(password)
            ).save()

            messages.success(request, 'User added successfully!')
            return redirect('/users/add')

        else:
            genderObj = Genders.objects.all()

            data = {
                'genders': genderObj
            }

            return render(request, 'user/addUser.html', data)
    except Exception as e:
        return HttpResponse(f'Error occured during add user: {e}')


def edit_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)

            # name of input is 'gender'
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthDate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')

            form_data = {
                'fullName': request.POST.get('full_name'),
                'gender': request.POST.get('gender'),
                'birthDate': request.POST.get('birth_date'),
                'address': request.POST.get('address'),
                'contactNumber': request.POST.get('contact_number'),
                'email': request.POST.get('email'),
                'username': request.POST.get('username'),
            }

            new_username = request.POST.get('username').strip()
        
            # Only check if username was changed
            if new_username != userObj.username:
                if Users.objects.filter(username__iexact=new_username).exists():
                    return render(request, 'user/editUser.html', {
                        'user': userObj,
                        'form_data': form_data,
                        'username_error': True
                    })
            
            # Update user if validation passes
            userObj.username = new_username
            userObj.full_name = fullName
            userObj.gender = Genders.objects.get(pk=gender)
            userObj.birth_date = birthDate
            userObj.address = address
            userObj.contact_number = contactNumber
            userObj.email = email
            userObj.username = username
            userObj.save()


            messages.success(request, 'Gender updated successfully!')
            # gabalik sa iban nga link
            return redirect('/users/list')

        
        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()

            data = {
                'user': userObj,
                'genders': genderObj
            }


            return render(request, 'user/editUser.html', data)
        
    except Exception as e:
        return HttpResponse(f'Error occured during edit user: {e}')


def delete_user(request, userId):
    try:
        if request.method == 'POST':
            userObj = Users.objects.get(pk=userId)
            userObj.delete()

            messages.success(request, 'User deleted successfully!')
            return redirect('/users/list')

        else:
            userObj = Users.objects.get(pk=userId)
            genderObj = Genders.objects.all()

            data = {
                'user': userObj,
                'genders': genderObj
            }


            return render(request, 'user/deleteUser.html', data)
    
    except Exception as e:
        return HttpResponse(f'Error occured during delete gender: {e}')

##
# def login(request):
#     global currentPassword
#     global currentUsername
#     try:
#         if request.method == 'POST':
#             users = Users.objects.all()
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             for i in users:
#                 if username == i.username and check_password(password, i.password):
#                   currentUsername = username
#                   currentPassword = password
#                   return redirect('user_list')
                
#             return render(request, 'user/login.html')    
#         else:
#             messages.error(request, 'Incorrect data!')
#             return render(request, 'user/login.html')
                    
#     except Exception as e:
#         return HttpResponse(f'Error occured during login: {e}')
# ##2
# def logout(request):
#     from django.contrib.auth import logout as auth_logout
#     auth_logout(request)
#     return redirect('login')


def search_users(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        users_result = Users.objects.filter(full_name__icontains=searched)

        p = Paginator(users_result, 10)
        page = request.GET.get('page')
        users = p.get_page(page)
        user_count = len(users_result)




        data = {
        'users_result': users_result,
        'users': users,
        'password': currentPassword,
        'username': currentUsername,
        'user_count': user_count,
        'searched': searched
        }
        
        return render(request, 'user/searchUser.html', {'searched': '', 'users': []})

def profile_page(request):
    users = Users.objects.get(username = currentUsername)
    data = {
        'users': users
	}
    return render(request, 'user/profile.html', data)
    

           
        

    #     return render(request, 'user/searchUser.html', data)
    # else:
    #     searched = request.GET.get('searched', '').strip()

    #     users_result = Users.objects.filter(full_name__icontains=searched)

    #     p = Paginator(users_result, 10)
    #     page = request.GET.get('page')
    #     users = p.get_page(page)
    #     user_count = len(users_result)




    #     data = {
    #     'users_result': users_result,
    #     'users': users,
    #     'password': currentPassword,
    #     'username': currentUsername,
    #     'user_count': user_count,
    #     'searched': searched
        
    #     }
        
    #     return render(request, 'user/searchUser.html', data)


def live_search(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            page_number = data.get('page', 1)
            
            # Search for users
            users_result = Users.objects.filter(full_name__icontains=query)
            total_count = users_result.count()
            
            # Paginate the results
            p = Paginator(users_result, 10)  # 10 users per page
            try:
                page_obj = p.page(page_number)
            except (EmptyPage, PageNotAnInteger):
                page_obj = p.page(1)
            
            # Prepare the data for JSON response
            users_data = []
            for user in page_obj:
                users_data.append({
                    'user_id': user.user_id,
                    'full_name': user.full_name,
                    'gender': user.gender.gender,
                    'birth_date': str(user.birth_date),
                    'address': user.address,
                    'contact_number': user.contact_number,
                    'email': user.email,
                    'username': user.username
                })
            
            # Prepare pagination data
            pagination_data = {
                'users': users_data,
                'current_page': page_obj.number,
                'num_pages': p.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'start_index': page_obj.start_index(),
                'end_index': page_obj.end_index(),
                'total_count': total_count
            }
            
            return JsonResponse(pagination_data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

user = ''

def login_view(request):
    global user

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('/users/list')  # Change to your desired redirect
        else:
            messages.error(request, 'Invalid username or password')
    
    

    return render(request, 'user/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')
