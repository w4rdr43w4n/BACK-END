from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from ath.serializers import check_password_validity
from django.views.decorators.csrf import csrf_exempt
from bd.settings import *

def login_page(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'log_in.html',{'message':message})
  else:
    return render(request,'log_in.html')

@login_required
def home(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'base.html',{'message':message})
  else:
    return render(request,'base.html')


def login_proc(request):
  usr = request.POST['usr']
  pwd = request.POST['pwd']
  user = authenticate(username=usr,password=pwd)
  if user is not None:
      login(request,user) 
      return message("home","Logged in successfully")
  else:
    return message("login","Username or password are incorrect, Try again or Signup!")

def signup_page(request):
  message = request.GET.get('message',None)
  if not message is None:
    return render(request,'sign_up.html',{'message':message})
  else:
    return render(request,'sign_up.html')

@csrf_exempt
def signup_proc(request):
  if request.method == "POST":
    usr = request.POST['usr']
    email = request.POST['email']
    pwd = request.POST['pwd']
    c_pwd = request.POST['pwdC']
    if pwd == c_pwd :
      if User.objects.filter(email=email).exists():
          return message('signup',"Email already taken, please enter another one")
      elif User.objects.filter(username=usr).exists():
        return message('signup',"Username is already taken, please enter another one")
      elif check_password_validity(pwd) != 'Valid' :
        val = check_password_validity(pwd)
        val = val[2:len(val)-2]
        errs = val.split("','")
        errs = " ".join(errs)
        return message('signup',errs)
      elif not usr.isalnum():
        return message('signup',"Username must be Alpha-numeric")
      else:
        user = User.objects.create_user(username=usr,email=email,password=pwd)
        user.save()
        send_email(usr,email)
        return message('login',"Account created successfully! please log in now.")
    else:
      return message('signup','Passwords did not match!')

def signup_redirect(request):
  return redirect('signup')

def login_redirect(request):
  return redirect('login')

def logout_proc(request):
  logout(request)
  return message('login','You logged out ,log in again please.')

def message(viewName:str,msg:str) -> HttpResponsePermanentRedirect:
  return redirect(reverse(viewName) + '?message=' + msg)

def send_email(user:str,email:str):
  subject = "Welcome to Our website!"
  message = str(f"Hi user:{user}, \n Thanks to login to our website! \n")
  from_email = EMAIL_HOST_USER
  to_list = [email]
  send_mail(subject,message,from_email,to_list,fail_silently=True)