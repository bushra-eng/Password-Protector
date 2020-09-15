from django.urls import path

from . import views

urlpatterns = [path("", views.m.home, name="home"),
               path('btn_login',views.m.btn_login, name='login'),
               path('btn_register',views.m.btn_register, name='register'),
               path('register',views.m.register,name='Sign_up'),
               path('login',views.m.login,name='Sign_in'),
               path('add',views.m.add_passw,name='Add_password'),
               path('adding_password',views.m.adding_password,name='Add'),
               path('viewing_password',views.m.viewing_password,name='View')]