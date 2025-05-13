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