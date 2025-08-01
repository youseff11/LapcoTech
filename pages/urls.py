from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

        # مسارات تسجيل الدخول والتسجيل والخروج
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('policies/', views.policies, name='policies'),
]
