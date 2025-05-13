from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Genders
from django.contrib import messages
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
  return render(request,'gender/addUser.html')


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