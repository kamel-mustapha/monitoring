from django.urls import path
from website.views import *
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('register/', Register.as_view() , name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page = "/")),
    path('pricing/', TemplateView.as_view(template_name = "offline/pricing.html"), name = "pricing"),
    path('activation/', TemplateView.as_view(template_name = "offline/activation.html")),
    path('activate-account/<int:user>/<str:code>', activate_account)
]

app_name = 'website'