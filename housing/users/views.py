from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .form import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from .utils import generate_otp, send_otp_email
from .models import CustomUser
def home(request):
    return render(request, 'base.html')
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html', {'section': 'dashboard'})
    
@login_required
def profile(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'account/profile.html')

@login_required
def properties(request):
    return render(request, 'account/properties.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_entered = request.data.get('otp')

        # Try to retrieve the user with matching email and OTP
        try:
            user = CustomUser.objects.get(email=email, otp=otp_entered)
            
            # Set the user's verification status to True
            user.is_verified = True
            user.save()

            # Return a response indicating success and a URL for the dashboard
            return Response({
                "message": "OTP verified successfully.",
                "redirect_url": "/dashboard"  # URL to redirect after successful OTP verification
            }, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            # If no user is found with the provided email and OTP, return an error
            return Response({
                "error": "Invalid OTP or email."
            }, status=status.HTTP_400_BAD_REQUEST)

       
class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_email(user.email, otp,user.username)
            return Response({"message": "User registered successfully. OTP sent to your email."}, status=status.HTTP_201_CREATED)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_page(request):
    return render(request, 'register.html')
def verify_page(request):
    return render(request, 'registration/verify.html')
