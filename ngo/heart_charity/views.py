from django.shortcuts import render
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from .models import Volunteer, Contact, Cause,Donate


# Create your views here.
def home(req):
    return render(req,'home.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # redirect to home or dashboard
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    return render(request, 'signin.html')



def validate_password(password):
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check maximum length
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")

    # Initialize flags for character checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    # Check for character variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )

    # Check against common passwords
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ]  # Add more common passwords
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

@csrf_protect
def signup_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        try:
            validate_password(password1)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(request, "signup.html", context)

        if not username or not password1 or not password2:
            context["errmsg"] = "Field can't be empty"
            return render(request, "signup.html", context)

        elif password1 != password2:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(request, "signup.html", context)

        elif username.isdigit():
            context["errmsg"] = "Username can't be only numbers"
            return render(request, "signup.html", context)

        elif password1 == username:
            context["errmsg"] = "Password cannot be the same as username"
            return render(request, "signup.html", context)
        else:
            try:
                userdata = User.objects.create_user(username=username, email=email, password=password1)
                userdata.save()
                return redirect("signin")
            except:
                context["errmsg"] = "User already exists"
                return render(request, "signup.html", context)

    return render(request, "signup.html")

def request_password_reset(req):
    if req.method == "GET":
        return render(req, "request_password_reset.html")
    else:
        uname = req.POST.get("uname")
        context = {}
        try:
            userdata = User.objects.get(username=uname)
            return redirect("reset_password", uname=userdata.username)

        except User.DoesNotExist:
            context["errmsg"] = "No account found with this username"
            return render(req, "request_password_reset.html",context)

def reset_password(req, uname):
    userdata = User.objects.get(username=uname)
    if req.method == "GET":
        return render(req, "reset_password.html", {"user": userdata.username})
    else:
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        userdata = User.objects.get(username=uname)
        try:
            if upass == "" or ucpass == "":
                context["errmsg"] = "Field can't be empty"
                return render(req, "reset_password.html", context)
            elif upass != ucpass:
                context["errmsg"] = "Password and confirm password need to match"
                return render(req, "reset_password.html", context)
            else:
                # validate_password(upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("signin")

        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "reset_password.html", context)


def our_causes(req):
    causes=Cause.objects.all()
    return render(req,'base.html',{"causes":causes})

def logout_view(req):
    logout(req)
    return redirect("home")