from django.shortcuts import render, redirect
#from django.http import HttpResponse 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from account.models import mlangles_user, mlangles_user_details
from django.contrib.auth.decorators import login_required
#from djano.contrib.auth import login

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        org = request.POST['org']
        org_mail = request.POST['org_mail']
        mobile = request.POST['mobile']
        pass_one = request.POST['pass_one']
        pass_two = request.POST['pass_two']

        if pass_one == pass_two:
            if User.objects.filter(email=org_mail).exists():
                messages.info(request, "Email exist")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username, email=org_mail, password=pass_one, first_name=fname, last_name=lname)
                user.save()
                mlangles_user_save = mlangles_user_details()
                mlangles_user_save.username = request.POST['username']
                mlangles_user_save.fname = request.POST['fname']
                mlangles_user_save.lname = request.POST['lname']
                mlangles_user_save.org = request.POST['org']
                mlangles_user_save.mobile = request.POST['mobile']
                mlangles_user_save.pass_one = request.POST['pass_one']
                mlangles_user_save.save()

                user_model = User.objects.get(username=username)
                new_profile = mlangles_user.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password not mactching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if  request.method == 'POST':
        username = request.POST['username']
        pass_one = request.POST['pass_one']

        user = auth.authenticate(username=username, password=pass_one)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect('signin')
    else:
        return render(request, 'login.html' )


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='signin')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html')