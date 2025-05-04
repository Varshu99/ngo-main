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

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile  # Make sure this is imported

def signin_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        selected_role = request.POST.get('role', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
                actual_role = profile.role

                if selected_role != actual_role:
                    messages.error(request, "Selected role doesn't match your account.")
                    return render(request, 'signin.html')

                login(request, user)

                if actual_role == 'admin':
                    print("Redirecting to admin dashboard")

                    return redirect('admin_dashboard')
                elif actual_role == 'volunteer':
                    return redirect('volunteer_dashboard')
                elif actual_role == 'user':
                    return redirect('user_dashboard')

            except Profile.DoesNotExist:
                messages.error(request, "User role not found. Contact support.")
        else:
            messages.error(request, "Invalid username or password.")

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

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Profile  # Ensure you have this import

@csrf_protect
def signup_view(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        role = request.POST.get("role", "")  # use get() for safety

        try:
            validate_password(password1)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(request, "signup.html", context)

        if not username or not password1 or not password2 or not role:
            context["errmsg"] = "Fields can't be empty"
            return render(request, "signup.html", context)

        elif password1 != password2:
            context["errmsg"] = "Password and confirm password don't match"
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

                # Create profile with role
                Profile.objects.create(user=userdata, role=role)

                return redirect("signin")

            except Exception as e:
                context["errmsg"] = "User already exists or another error occurred"
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



def logout_view(req):
    logout(req)
    return redirect("home")


    

def admin_dashboard(request):
    users = []  # or users = None, depending on your logic

    if request.method == "POST":
        users = User.objects.all()

    return render(request, "admin_dashboard.html", {"users": users})

from django.shortcuts import render
from .models import Event
from datetime import datetime
from django.shortcuts import render, get_object_or_404

def volunteer_dashboard(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        event = get_object_or_404(Event, id=event_id)
        event.participant_count += 1
        event.save()
        return JsonResponse({'count': event.participant_count})
    
    upcoming_events = Event.objects.filter(start_time__gte=datetime.now()).order_by('start_time')

    return render(request, 'volunteer_dashboard.html', {'events': upcoming_events})



def user_dashboard(req):
    causes = Cause.objects.all()
    return render(req, 'user_dashboard.html', {"causes": causes})  


# def donate(request,id):
#     if request.method =="POST":
#         name=request.POST['name']
#         email=request.POST['email']
#         amount=request.POST.get('amount')

#         cause=Cause.objects.get(id=id)
#         cause.raised=cause.raised+float(amount)
#         cause.goal=cause.goal-float(amount)
#         cause.save()
#         donation=Donate.objects.create(name=name,email=email,amount=float(amount))
#         donation.save()
#         return redirect('donate')
#     else:
#         cause=Cause.objects.get(id=id)
#         return render(request,'donate.html',{"cause":cause})

import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Cause

def donate(request, id):
    cause = get_object_or_404(Cause, id=id)

    remaining_amount = cause.goal - cause.raised

    if remaining_amount <= 0:
        return render(request, 'donate.html', {
            'cause': cause,
            'error': "This cause has already met its goal. Thank you!"
        })

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    amount = int(remaining_amount * 100)  # in paise

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        'cause': cause,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    }

    return render(request, 'donate.html', context)

# views.py


# def calendar_view(request):
#     upcoming_events = Event.objects.filter(start_time__gte=datetime.now()).order_by('start_time')
#     return render(request, 'calendar.html', {'events': upcoming_events})
