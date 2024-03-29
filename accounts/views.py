from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from urllib.parse import parse_qs,urlparse

# Create your views here.


def signup(request):
    if request.method=='POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'username has already been taken ...!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html',{'error':'passwords must be match...!'})
    else:
        return render(request,'accounts/signup.html')

def login(request):
    if request.method=='POST':
        user=auth.authenticate( username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if 'next' in request.META.get('HTTP_REFERER'):
                redirecturl = parse_qs(urlparse(request.META.get('HTTP_REFERER')).query)
                auth.login(request, user)
                return redirect(redirecturl['next'][0])
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html',{'error':'username or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('login')
    return redirect('home')
