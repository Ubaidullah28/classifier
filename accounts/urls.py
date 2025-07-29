from django.urls import path
from . import views
from .views import dashboard_view



urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', dashboard_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('update-user/', views.update_user_view, name='update_user'),
    path('add_user', views.add_user_view, name='add_user'),
     # New URLs for category/subcategory management
    path('update-category/', views.update_category_view, name='update_category'),
    path('update-subcategory/', views.update_subcategory_view, name='update_subcategory'),
    path('add-category/', views.add_category_view, name='add_category'),
    path('add-subcategory/', views.add_subcategory_view, name='add_subcategory'),

    
]
