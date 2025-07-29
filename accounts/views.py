

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import backend
from .backend import update_user, add_user



# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

       
#         if backend.check_user(email, password):
          
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid email or password.')

#     return render(request, 'accounts/login.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data = backend.check_user(email, password)
        if user_data:
            # user_data structure: (UserId, Email, FirstName, LastName, Password, isAdmin)
            is_admin = user_data[5]  # isAdmin is at index 5
            
            # Store user info in session
            request.session['user_id'] = user_data[0]
            request.session['user_email'] = user_data[1]
            request.session['user_first_name'] = user_data[2]
            request.session['user_last_name'] = user_data[3]
            request.session['is_admin'] = is_admin
            
            # Redirect based on admin status
            if is_admin:
                return redirect('settings')  # Redirect admin to settings page
            else:
                return redirect('home')  # Redirect regular user to dashboard
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')



def dashboard_view(request):
   return render(request, 'accounts/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def settings_view(request):
    users = backend.fetch_all_users()
    return render(request, 'accounts/settings.html', {'users': users})


def update_user_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        backend.update_user(user_id, email, first_name, last_name, password)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})



@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        data = request.POST
        add_user(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password']
        )
        return JsonResponse({'status': 'success'})