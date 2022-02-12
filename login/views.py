from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.contrib import messages, auth


def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            return redirect('login')
    return render(request, 'accounts/login.html')



def register(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                    username=username, password=password)
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in.')
                    user.save()
                    messages.success(request, 'You are registered successfully.')
                    return redirect('dashboard')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dash.html')

@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return redirect('login')