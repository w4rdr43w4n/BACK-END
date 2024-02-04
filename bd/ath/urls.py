from django.urls import  path,include
from . import views

urlpatterns = [
    # main account page
    path('',views.home,name='home'),
    # sign up and log in pages
    path('signup/',views.signup_page,name='signup'),
    path('login/',views.login_page,name='login'),
    # sign up and log in processors pages
    path('signup/signup_proc/',views.signup_proc,name='sign_up_proc'),
    path('login/login_proc/',views.login_proc,name='log_in_proc'),
    # sign up and log in pages redirectors
    path('login/signup/',views.signup_redirect,name='sign_up_redirect'),
    path('signup/login/',views.login_redirect,name='log_in_redirect'),
    # Google sign in
    path('logout/',views.logout_proc,name='logout'),
    path('social-auth/', include('social_django.urls',namespace='social')),
]
