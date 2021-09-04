from django.contrib import admin 
from django.urls import path 
from . import views
from django.conf.urls import url


app_name='create_org'

urlpatterns= [
	path('home/', views.home, name='home' ),
    path('login/', views.login_view, name='login'),
    path('signin/',views.signin_view, name='signin'),
    path('landing/', views.landing_page, name='landing'),
    path('logout/',views.logout_view, name='logout'),
    path('new_org/', views.new_org, name='new_org'),
    path('view_org/', views.view_org , name='view_org'),
    path('organisation/<str:name>/', views.organisation , name='organisation'),
    path('update_org/<str:name>/delete', views.del_org , name='del_org'),
    #members Model
    path('update_org/<str:name>/add_user', views.add_user , name='add_user'),
    path('update_org/<str:name>/members' , views.org_members , name='org_members'),
    path('update_org/<str:name>/members/delete' , views.delete_members , name='del_members'),
    #ajax
    path('fetch_member/', views.fetch_member, name='fetch_member')
	
	

]



