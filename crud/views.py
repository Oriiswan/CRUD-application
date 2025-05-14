from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Genders, Users
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login

from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator


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
		userObj = Users.objects.select_related('gender')

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


def login(request):
    global currentPassword
    global currentUsername
    try:
        if request.method == 'POST':
            users = Users.objects.all()
            username = request.POST.get('username')
            password = request.POST.get('password')
            for i in users:
                if username == i.username and check_password(password, i.password):
                  currentUsername = username
                  currentPassword = password
                  return redirect('user_list')
                
            return render(request, 'user/login.html')    
        else:
            return render(request, 'user/login.html')
                    
    except Exception as e:
        return HttpResponse(f'Error occured during login: {e}')

def logout(request):
    logout(request)
    return redirect('login')
