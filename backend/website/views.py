import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from .forms import UserForm
from .models import *
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from api.models import UserPage
from django.http import Http404
from django.conf import settings


class Home(View):
    def get(self, req, *args, **kwargs):
        if req.user.is_authenticated:
            response = render(req, 'online/index.html')
            response.set_cookie("API_KEY", req.user.api_key)
            return response
        else:
            return render(req, 'offline/home.html')
        # return JsonResponse({}, status=404)

class Login(View):
    def get(self, req, *args, **kwargs):
        if not req.user.is_authenticated:
            return render(req, 'offline/login.html')
        else:
            return redirect('website:home')
    def post(self, req, *args, **kwargs):
        res = {'status': 'error', 'message': 'unknown error'}
        try:
            req_data = json.loads(req.body)
            user = authenticate(username = req_data.get('username'), password = req_data.get('password'))
            if user is not None:
                login(req, user)
                res["status"] = "success"
                res["message"] = "Successful login"
            else: 
                res['errors'] = "Wrong credentials or account not activated"
        except Exception as e:
            print(e)
        return JsonResponse(res)

class Register(View):
    def get(self, req, *args, **kwargs):
        if not req.user.is_authenticated:
            return render(req, 'offline/register.html')
        else:
            return redirect('website:home')
    def post(self, req, *args, **kwargs):
        res = {'status': 'error', 'message': 'unknown error'}
        try:
            req_data = json.loads(req.body)
            user_form = UserForm(data=req_data)
            if user_form.is_valid():
                new_user = user_form.save()
                new_user.is_active = False
                new_user.save()
                res['status'] = 'success'
                res['message'] = 'Successful registration'
                activation_code = Activation.objects.create()
                website = "http://localhost:8000" if settings.DEBUG else "https://statuschecks.net"
                send_mail(
                    'Account Activation',
                    'Click on the link to activate your account.',
                    'musk96.km@gmail.com',
                    [new_user.email],
                    fail_silently=False,
                    html_message=f'<a href = "{website}/activate-account/{new_user.id}/{activation_code.code}">Click here</a>'
                )
            else:
                errors = user_form.errors.values()
                res['errors'] = list(errors)
                del res['message']
        except Exception as e:
            print(e)
        return JsonResponse(res)


def activate_account(req, user, code):
    activation_code = Activation.objects.filter(Q(code = code) & Q(used = False))
    activation_user = User.objects.filter(id = user)
    if activation_code and activation_user:
        activation_user[0].is_active = True
        activation_code[0].used = True
        activation_user[0].save()
        activation_code[0].save()
        # login(req, activation_user[0])
    return redirect('website:login')


def user_monitor(req, id):
    page = UserPage.objects.filter(id=id)
    if page:
        page = page[0]
        context = {
            "PAGE_ID": id,
            "PAGE_TITLE": page.title,
            "PAGE_LINK": page.href_link,
            "PAGE_ICON": page.icon_link,
            "PAGE_NAME": page.name
        }
        page.seen += 1
        page.save()
        return render(req, f"monitors/{page.page.html_file}.html", context=context)
    raise Http404