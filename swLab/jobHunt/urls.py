"""
urls.py
------------------------------------------------------------
Takes the url request made by the user and redirect it to the corresponding views
"""

from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('search',views.search,name='search'),
    path('login',views.login,name='login'),
    path('verify_login',views.verify_login,name='verify_login'),
    path('verify_register',views.verify_register,name='verify_register'),
    path('make_update',views.make_update,name='make_update'),
    path('register',views.register,name='register'),
    path('update',views.update,name='update'),
    path('logout',views.logout,name='logout'),
    path('*',views.index,name="default")
]
