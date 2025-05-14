from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Genders, Users
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Create your views here.


def addGender(request):
  try:
    if request.method == 'POST':
      gender = request.POST.get('gender')
      
      Genders.objects.create(gender = gender).save()
      messages.success(request, 'Gender added successfully')
      return redirect('/gender/list')
    else:
       return render(request, 'gender/addGender.html')
  except Exception as e:
    return HttpResponse('Error has been occured')
 
 
def genderList(request):
  try:
    gender = Genders.objects.all() # SELECT * FROM tbl_genders
    data = {
      'genders': gender
    }
    return render(request, 'gender/genderList.html', data)
  except Exception as e:
    return HttpResponse(f'Eroor occured during load genders: {e}')
    
  
 
def addUser(request):
  return render(request,'user/addUser.html')


def editGender(request, genderId):
  try:
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk = genderId)
      gender = request.POST.get('gender')
      
      genderObj.gender = gender
      genderObj.save()
      messages.success(request, 'Edit gender successfully')
      
      data = {
        'gender': genderObj
      }
      
      return render(request, 'gender/editGender.html', data)
      
    else:
      genderObj = Genders.objects.get(pk = genderId)
      
      data = {
        'gender': genderObj
      }
      
      return render(request, 'gender/editGender.html', data)
  except Exception as e:
   return HttpResponse(f'Error has been occurred: {e}') 
 
def deleteGender(request, genderId):
  try:
    if request.method == 'POST':
      genderObj = Genders.objects.get(pk =genderId)
      
      genderObj.delete()
      genderObj.save
      messages.success(request, 'Record has been deleted')
      
      
      data = {
        'gender' : genderObj
      }
      
      return render(request, 'gender/deleteGender.html', data)
    else:
      genderObj = Genders.objects.get(pk =genderId)
      
      
      data = {
        'gender' : genderObj
      }
      
      return render(request, 'gender/deleteGender.html', data)
  except Exception as e:
    return HttpResponse(f'Error has been Occurred: {e}')
  
def userList(request):
  # return render(request, 'user/userList.html')
  try:
    userObj = Users.objects.select_related('gender')

    data = {
      'users': userObj
    }

    return render(request, 'user/userList.html', data)
  
  except Exception as e:
    return HttpResponse(f'Error occured during load users: {e}')
  
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

			# if password != confirmPassword:

			Users.objects.create(
				full_name = fullName,
				gender = Genders.objects.get(pk=gender),
				birth_date = birthDate,
				address = address,
				contact_number = contactNumber,
				email = email,
				username = username,
				password = make_password(password)
			).save()

			messages.success(request, 'User added successfully!')
			return redirect('/users/add')

		else:
			genderObj = Genders.objects.all()

			data = {
				'genders': genderObj
			}

			return render(request, 'user/AddUser.html', data)
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
			return redirect('/user/userlist')

		
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
			return redirect('/user/userlist')

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