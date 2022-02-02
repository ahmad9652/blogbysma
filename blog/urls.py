from unicodedata import name
from django import views
from django.urls import path
from blog import views

urlpatterns = [
    path('',views.index,name="home"),
    path('blog1/',views.blog1,name="blog"),
    path('blogpost/<str:Slug>',views.blogpost,name="blogpost"),
    path('postcomment/',views.postcomment,name='comment'),
    path('contactus/',views.contact,name="contact"),
    path('search/',views.search,name='search'),
    path('handlesignup/',views.handlesignup,name='signup'),
    path('login/',views.handlelogin,name='login'),
    path('logout/',views.handlelogout,name='logout'),
    path('dashboard/',views.handleuserdashboard,name="userdashboard"),
    path('createblog/',views.usercreatedblog,name="userblog")
    
]