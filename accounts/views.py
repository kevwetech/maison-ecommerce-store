from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings  # ADD THIS
from .forms import RegistrationForm, UserUpdateInfoForm, PasswordChangeForm
from .models import CustomUser, PasswordResetOTP, EmailVerificationOTP
import random
import threading
from django.utils import timezone
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




def send_email_async(subject, message, from_email, recipient_list):
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        for recipient in recipient_list:
            mail = Mail(
                from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                to_emails=recipient,
                subject=subject,
                plain_text_content=message
            )
            response = sg.client.mail.send.post(request_body=mail.get())
            print(f"Email status: {response.status_code}")
    except Exception as e:
        print(f"Email error: {e}")

# Signup
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = str(random.randint(100000, 999999))
            EmailVerificationOTP.objects.filter(user=user).delete()
            EmailVerificationOTP.objects.create(user=user, otp=otp)
            send_email_async(
                subject='Verify your Maison account',
                message=f'Hi {user.full_name},\n\nYour verification code is: {otp}\n\nThis code expires in 10 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,  # CHANGED - use settings
                recipient_list=[user.email],
            )

            request.session['verify_email'] = user.email
            return redirect('verify_email_otp')
        else:
            print("FORM ERRORS:", form.errors)
            messages.error(request, "This email is already in use.")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def verify_email_otp(request):
    email = request.session.get('verify_email')
    if not email:
        return redirect('signup')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = EmailVerificationOTP.objects.filter(user=user, otp=otp).last()
            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                user.is_active = True
                user.email_verified = True
                user.save()
                del request.session['verify_email']
                return redirect('verify_email_done')
            else:
                messages.error(request, 'Invalid or expired code.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Something went wrong.')
    return render(request, 'accounts/verify_email_otp.html')


def verify_email_done(request):
    return render(request, 'accounts/verify_email_done.html')


# Login
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # ✅ FIX
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.full_name}!")
            return redirect('homepage')
        else:
            # 🔥 CHECK IF USER EXISTS BUT IS NOT VERIFIED
            try:
                user = CustomUser.objects.get(email=email)

                if not user.is_active:
                    messages.error(request, "Please verify your email before logging in.")
                    request.session['verify_email'] = email
                    return redirect('verify_email_otp')

            except CustomUser.DoesNotExist:
                pass

            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


# Logout
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def userupdateinfo(request):
    form = UserUpdateInfoForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, 'There was an error updating your profile.')
    return render(request, 'accounts/userupdateinfo.html', {'form': form})


@login_required
def userchangepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/userchangepassword.html', {'form': form})


@login_required
def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.create(user=user, otp=otp)
            send_email_async(
                subject='Your Maison Password Reset Code',
                message=f'Hi {user.full_name},\n\nYour password reset code is: {otp}\n\nThis code expires in 10 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,  # CHANGED - use settings
                recipient_list=[user.email],
            )
            request.session['reset_email'] = email
            return redirect('password_reset_verify')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'accounts/password_reset.html')


def password_reset_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('reset_email')
        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
            if otp_obj and otp_obj.is_valid():
                otp_obj.is_used = True
                otp_obj.save()
                request.session['reset_verified'] = True
                return redirect('password_reset_confirm_otp')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Something went wrong.')
    return render(request, 'accounts/password_reset_verify.html')


def password_reset_confirm_otp(request):
    if not request.session.get('reset_verified'):
        return redirect('password_reset')
    if request.method == 'POST':
        password1 = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            email = request.session.get('reset_email')
            user = CustomUser.objects.get(email=email)
            user.set_password(password1)
            user.save()
            del request.session['reset_email']
            del request.session['reset_verified']
            messages.success(request, 'Password changed successfully!')
            return redirect('login')
    return render(request, 'accounts/password_reset_confirm.html')


@login_required
def account_settings(request):
    return render(request, 'accounts/account_settings.html', {'user': request.user})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('signup')