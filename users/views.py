import logging
from uuid import uuid4

from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from . import sms

from .models import User
from .utils import generate_code, cryptography_fearnet_encoder

# Create your views here.

logger = logging.getLogger(__name__)


def loginView(request) -> dict:
    if request.user.is_authenticated and request.user.is_verified:
        return redirect('home')

    page: str = 'login'
    code: str = generate_code()
    user: User = None 

    if request.metho == 'POST':
        phone = request.POST.get('phone').replace('+', '')

        try:
            with transaction.atomic():
                user = User.objects.get(phone=phone, is_deleted=False)
                if user is not None:
                    user.is_verified = False
                    sms._send_verify_message(user.phone, code)
                    user.save()
                    context: dict = {
                        'request': request,
                        'user': user,
                        'code': code,
                    }
                    login(**context)
                    return redirect('confirm')
        except User.DoesNotExist:
            page: str = 'register'
    
    context: dict = {
        "page": page
    }

    return redirect(request, 'users/login.html', context)


def registerView(request) -> dict:
    if request.user.is_authenticated and request.user.is_verified:
        return redirect('home')
        
    if request.method == 'POST':
        context: dict = {}
        password, key = cryptography_fearnet_encoder(str(uuid4)).replace('-', '')[:12]


        try:
            context['key'] = key 
            context['password'] = password.decode()
            context['full_name'] = request.POST.get('name')
            context['phone'] = request.POST.get('phone_number').replace('+', '')

            code:str = generate_code()

            try:
                user: User = User.objects.get(phone=context['phone'])
                if user.is_authenticated and user.is_verified:
                    return redirect('home')

                sms._send_verify_message(user.phone, code)
                context: dict = {
                    "user": user,
                    "code": code,
                    "request": request,
                }
                if user.is_authenticated and user.is_verified==False:
                    login(**context)
                    return redirect('confirm')
            except User.DoesNotExist:
                logger.info("User does not exist")

            user: User = User.objects.create(**context)
            with transaction.atomic():
                if user is not None:
                    user.is_verified = False
                    sms._send_verify_message(user.phone, code)
                    user.save()
                    context: dict = {
                        "request": request,
                        "user": user,
                        "code": code,
                    }
                    login(**context)

                return redirect('confirm')

        except Exception as e:
            context: dict = {
                "text": e,
            }
            print(**context)
            pass

    return render(request, 'users/login.html')


def verifyView(request) -> None:
    page: str = 'confirm'
    code: request.POST.get('code')
    session_id: str = request.COOKIES.get('sessionid')

    try:
        if True:
            pass

    except Exception as e:
        pass 



