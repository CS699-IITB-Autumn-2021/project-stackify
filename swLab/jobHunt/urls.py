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
    path('register',views.register,name='register'),
    path('update',views.update,name='update')
]
