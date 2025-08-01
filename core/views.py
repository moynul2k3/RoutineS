from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
UserAccount = get_user_model() # adjust import as needed
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

from django.utils.crypto import get_random_string

def sign_in(request):
    if request.method == 'POST':
        identifier = request.POST.get('email')  # this field holds email or REG_no
        password = request.POST.get('password')

        # Try to authenticate by email
        user = authenticate(request, email=identifier, password=password)

        # If not authenticated by email, try by REG_no
        if user is None:
            user = authenticate(request, REG_no=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('/')  # change to your landing page
        else:
            messages.error(request, 'Invalid credentials, please try again.')
    return render(request, 'signin.html') 




def sign_up(request):
    departments = Department.objects.all()
    universities = University.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        REG_no = request.POST.get('reg')
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        batch_id = request.POST.get('batch')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'sign_up.html', {'universities': universities})
            # return render(request, 'sign_up.html', {'departments': departments})

        try:
            # Optional: You can also validate if department and batch exist
            university = University.objects.get(id=university_id)
            department = Department.objects.get(id=department_id)
            batch = Batch.objects.get(id=batch_id)

            user = UserAccount.objects.create_user(
                email=email,
                REG_no=REG_no,
                password=password,
                name=name,
                university = university,
                department = department,
                batch = batch
            )

            messages.success(request, 'Account created successfully.')
            user.backend = 'core.backends.AuthBackend'
            login(request, user)
            return redirect('/')
        except IntegrityError:
            messages.error(request, 'Email or REG_no already exists.')
        except Department.DoesNotExist:
            messages.error(request, 'Invalid department selected.')
        except Batch.DoesNotExist:
            messages.error(request, 'Invalid batch selected.')

    return render(request, 'sign_up.html', {'departments': departments, 'universities': universities})


def get_department(request, university_id):
    department = Department.objects.filter(university_id=university_id).order_by('name')
    department_data = [{'id': d.id, 'name': d.name} for d in department]
    return JsonResponse({'department': department_data})

def get_batches(request, department_id):
    batches = Batch.objects.filter(department_id=department_id).order_by('-name')
    batch_data = [{'id': b.id, 'name': b.name} for b in batches]
    return JsonResponse({'batches': batch_data})


def logout_view(request):
    logout(request)
    return redirect('/')



@login_required(login_url='signin') 
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.name = request.POST.get('name')
        # user.email = request.POST.get('email')
        user.reg = request.POST.get('reg')
        user.university_id = request.POST.get('university')
        user.department_id = request.POST.get('department')
        user.batch_id = request.POST.get('batch')
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('home')

    universities = University.objects.all()
    departments = Department.objects.filter(university=user.university) if user.university else []
    batches = Batch.objects.filter(department=user.department) if user.department else []

    return render(request, 'edit_profile.html', {
        'universities': universities,
        'departments': departments,
        'batches': batches,
        'user': user,
    })






@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        otp = random.randint(100000, 999999)

        # Store in session (you could use DB or cache too)
        request.session['otp'] = str(otp)
        request.session['user_info'] = {
            "name": data.get("name"),
            "email": email,
            "password": data.get("password"),
        }
        print('Verify OTP: ',otp)


        html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 20px;">
                    <table align="center" width="100%" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #4a3aff; color: #ffffff; border-radius: 8px 8px 0 0;">
                                <h1>RoutineS - Email Verification</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 20px; text-align: left; color: #333333;">
                                <p>Hi there,</p>
                                <p>Thank you for signing up with <strong>RoutineS</strong>. Please verify your email address by using the OTP below:</p>
                                <p style="text-align: center; margin: 30px 0;">
                                    <span style="display: inline-block; padding: 12px 24px; background-color: #4a3aff; color: #ffffff; border-radius: 6px; font-size: 24px; font-weight: bold; letter-spacing: 2px;">
                                        {otp}
                                    </span>
                                </p>
                                <p>This OTP is valid for only <strong>5 minutes</strong>. Please do not share it with anyone.</p>
                                <br>
                                <p>Thanks,<br>The RoutineS Team</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; text-align: center; font-size: 12px; color: #999999;">
                                <p>&copy; 2024 RoutineS. All rights reserved.</p>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
        """

        plain_message = f"""
            Hi,

            Thank you for registering with RoutineS.
            Please verify your email address to complete the registration process.

            Your OTP for registration on RoutineS is:

            {otp}

            This OTP is valid for only 5 minutes. Please do not share it with anyone.

            If you did not initiate this request, please ignore this email.

            Thanks,
            The RoutineS Team
        """


        send_mail(
            subject="Your OTP Code",
            message=plain_message,  # Fallback plain text
            from_email="noreply@routines.moynul.com",
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message  # The HTML version
        )

        return JsonResponse({"status": "ok"})

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body)
        otp = data.get("otp")

        if otp == request.session.get("otp"):
            return JsonResponse({"status": "verified"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid OTP"})
        





OTP_SESSION_KEY = "forgot_password_otp"

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not UserAccount.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email not registered"}, status=400)

        otp = get_random_string(length=6, allowed_chars='1234567890')
        request.session[OTP_SESSION_KEY] = {"email": email, "otp": otp}

        html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 20px;">
                    <table align="center" width="100%" style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <tr>
                            <td style="padding: 20px; text-align: center; background-color: #4a3aff; color: #ffffff; border-radius: 8px 8px 0 0;">
                                <h1>RoutineS - Password Reset</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 20px; text-align: left; color: #333333;">
                                <p>Hi there,</p>
                                <p>You requested to reset your password for your <strong>RoutineS</strong> account.</p>
                                <p style="text-align: center; margin: 30px 0;">
                                    <span style="display: inline-block; padding: 12px 24px; background-color: #4a3aff; color: #ffffff; border-radius: 6px; font-size: 24px; font-weight: bold; letter-spacing: 2px;">
                                        {otp}
                                    </span>
                                </p>
                                <p>This OTP is valid for only <strong>5 minutes</strong>. Please do not share it with anyone.</p>
                                <p>If you did not request a password reset, please ignore this email or contact support.</p>
                                <br>
                                <p>Thanks,<br>The RoutineS Team</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; text-align: center; font-size: 12px; color: #999999;">
                                <p>&copy; 2024 RoutineS. All rights reserved.</p>
                            </td>
                        </tr>
                    </table>
                </body>
            </html>
            """

        plain_message = f"""
            Hi,

            You requested to reset your password for your RoutineS account.

            Your OTP to reset your password is:

            {otp}

            This OTP is valid for only 5 minutes. Please do not share it with anyone.

            If you did not request a password reset, please ignore this email or contact support.

            Thanks,
            The RoutineS Team
        """

        send_mail(
            subject="RoutineS - Password Reset OTP",
            message=plain_message,
            from_email="noreply@routines.com",
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return JsonResponse({"status": "ok", "message": "OTP sent"})

    return render(request, "forgot_password.html")



OTP_SESSION_KEY = "forgot_password_otp"

def verify_forgot_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            otp = data.get("otp")
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        session_data = request.session.get(OTP_SESSION_KEY)

        if not session_data:
            return JsonResponse({"status": "error", "message": "No OTP session found"}, status=400)

        if otp == session_data.get("otp"):
            return JsonResponse({"status": "verified", "message": "OTP verified"})

        return JsonResponse({"status": "error", "message": "Invalid OTP"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


# @csrf_exempt
def reset_password(request):
    new_password = request.POST.get("new_password")
    confirm_password = request.POST.get("confirm_password")
    session_data = request.session.get(OTP_SESSION_KEY)

    if not session_data:
        return JsonResponse({"status": "error", "message": "No session found"}, status=400)

    if new_password != confirm_password:
        return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

    try:
        user = UserAccount.objects.get(email=session_data.get("email"))
        user.set_password(new_password)
        user.save()
        del request.session[OTP_SESSION_KEY]
        return JsonResponse({"status": "ok", "message": "Password reset successfully"})
    except UserAccount.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User not found"}, status=400)