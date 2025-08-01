

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import backend
import os
from django.conf import settings
from .backend import update_user, add_user
from . import backend



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user_data = backend.check_user(email, password)
        if user_data:
            # user_data structure: (UserId, Email, FirstName, LastName, Password, isAdmin)
            user_id, user_email, first_name, last_name, _, is_admin = user_data

            # Store user info in session
            request.session['user_id'] = user_id
            request.session['user_email'] = user_email
            request.session['user_first_name'] = first_name
            request.session['user_last_name'] = last_name
            request.session['is_admin'] = bool(is_admin)

            # Redirect based on admin status
            if bool(is_admin):
                return redirect('home')  # You must have a URL named 'settings'
            else:
                return redirect('home')  # You must have a URL named 'home'
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')



# def dashboard_view(request):
#    return render(request, 'accounts/dashboard.html')


def dashboard_view(request):
    is_admin = request.session.get('is_admin', False)
    return render(request, 'accounts/dashboard.html', {
        'is_admin': is_admin
    })



def logout_view(request):
    logout(request)
    return redirect('login')


# def settings_view(request):
#     users = backend.fetch_all_users()
#     return render(request, 'accounts/settings.html', {'users': users})


from django.http import HttpResponseForbidden

def settings_view(request):
    users = backend.fetch_all_users()

    if not request.session.get('is_admin', False):
        return HttpResponseForbidden("Access Denied: Admins only.")

    return render(request, 'accounts/settings.html', {'users' : users})



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
    



@csrf_exempt
def update_category_view(request):
    """Update category name"""
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            new_category_name = request.POST.get('new_category_name')
            
            # Get category by name
            category_data = backend.get_category_by_name(category_name)
            if category_data:
                category_id = category_data[0]
                success = backend.update_category(category_id, new_category_name)
                if success:
                    return JsonResponse({'status': 'success', 'message': 'Category updated successfully'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to update category'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Category not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def update_subcategory_view(request):
    """Update subcategory name and description"""
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            subcategory_name = request.POST.get('subcategory_name')
            new_subcategory_name = request.POST.get('new_subcategory_name')
            new_description = request.POST.get('new_description')
            
            # Get category first
            category_data = backend.get_category_by_name(category_name)
            if category_data:
                category_id = category_data[0]
                # Get subcategory
                subcategory_data = backend.get_subcategory_by_name(subcategory_name, category_id)
                if subcategory_data:
                    subcategory_id = subcategory_data[0]
                    success = backend.update_subcategory(subcategory_id, new_subcategory_name, new_description)
                    if success:
                        return JsonResponse({'status': 'success', 'message': 'Subcategory updated successfully'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Failed to update subcategory'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Subcategory not found'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Category not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def add_category_view(request):
    """Add new category"""
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            if not category_name:
                return JsonResponse({'status': 'error', 'message': 'Category name is required'})
            
            category_id = backend.add_category(category_name)
            if category_id:
                return JsonResponse({'status': 'success', 'message': 'Category added successfully', 'category_id': category_id})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to add category'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def add_subcategory_view(request):
    """Add new subcategory"""
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
            subcategory_name = request.POST.get('subcategory_name')
            description = request.POST.get('description')
            
            if not all([category_name, subcategory_name, description]):
                return JsonResponse({'status': 'error', 'message': 'All fields are required'})
            
            # Get category first
            category_data = backend.get_category_by_name(category_name)
            if category_data:
                category_id = category_data[0]
                subcategory_id = backend.add_subcategory(category_id, subcategory_name, description)
                if subcategory_id:
                    return JsonResponse({'status': 'success', 'message': 'Subcategory added successfully', 'subcategory_id': subcategory_id})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to add subcategory'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Category not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@csrf_exempt
def refresh_json_view(request):
    """Regenerate the data.json file from database"""
    try:
        # Use the existing fakejson.py logic
        conn = backend.get_connection()
        cursor = conn.cursor()
        
        # Fetch data from database
        query = """
            SELECT
                CC."CategoryName",
                CS."SubCategoryName",
                CS."Description"
            FROM
                "Classifier"."Category" CC
            LEFT JOIN
                "Classifier"."SubCategory" CS
            ON
                CC."CategoryId" = CS."SubCategoryCategoryId"
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Transform to nested JSON
        category_map = {}
        for CategoryName, SubCategoryName, Description in rows:
            if CategoryName not in category_map:
                category_map[CategoryName] = []
            if SubCategoryName is not None:
                category_map[CategoryName].append({
                    "SubCategoryName": SubCategoryName,
                    "Description": Description
                })
        
        result = [
            {
                "CategoryName": cat,
                "SubCategory": subs
            }
            for cat, subs in category_map.items()
        ]
        
        # Write to JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'accounts', 'data.json')
        with open(json_file_path, 'w') as f:
            json.dump(result, f, indent=4)
        
        cursor.close()
        conn.close()
        return JsonResponse({'status': 'success', 'message': 'JSON file refreshed successfully'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    










from django.http import JsonResponse
from django.db import connection

def fetch_category_data(request):
    query = """
        SELECT
            CC."CategoryName",
            CS."SubCategoryName",
            CS."Description"
        FROM
            "Classifier"."Category" CC
        LEFT JOIN
            "Classifier"."SubCategory" CS
        ON
            CC."CategoryId" = CS."SubCategoryCategoryId"
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    category_map = {}
    for CategoryName, SubCategoryName, Description in rows:
        if CategoryName not in category_map:
            category_map[CategoryName] = []
        if SubCategoryName:
            category_map[CategoryName].append({
                "SubCategoryName": SubCategoryName,
                "Description": Description
            })

    result = [
        {
            "CategoryName": cat,
            "SubCategory": subs
        }
        for cat, subs in category_map.items()
    ]

    return JsonResponse(result, safe=False)