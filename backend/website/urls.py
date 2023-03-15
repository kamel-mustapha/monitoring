from django.urls import path, re_path
from website.views import *
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


ANGULAR_PATHS = ["dashboard", "pages", "profile", "plans"]

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view() , name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page = "/")),
    path('activation/', TemplateView.as_view(template_name = "offline/activation.html")),
    path('activate-account/<int:user>/<str:code>', activate_account),
    path('monitor/<int:id>', user_monitor),
]

for url_path in ANGULAR_PATHS:
    urlpatterns.append(
        path(f"{url_path}", login_required(TemplateView.as_view(template_name="online/index.html")))
    )

app_name = 'website'