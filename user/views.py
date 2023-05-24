from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Profile
# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username=username)
            newUser.set_password(password)
            newUser.save()

            profile = Profile(user=newUser)
            profile.save()

            login(request, newUser)
            messages.success(request, "You have successfully registered.")
            return redirect("index")
        context = {
            "form":form
        }
        return render(request, "register.html", context)
    else:
        form = RegisterForm()
        context = {
            "form":form
        }
        return render(request, "register.html", context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        usernam = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=usernam, password=password)
        if user is None:
            messages.info(request, "Username or password is wrong.")
            return render(request, "login.html", context)
        messages.success(request, "You have successfully logged in.")
        login(request, user)
        return redirect("index")
    return render(request, 'login.html', context)




def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("index")

