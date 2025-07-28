from django.urls import path
from . import views
from .views import dashboard_view


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', dashboard_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.settings_view, name='settings'),
    path('update-user/', views.update_user_view, name='update_user'),
    path('add_user', views.add_user_view, name='add_user'),
    
]
