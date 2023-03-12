from django.urls import path
from payment.views import *

urlpatterns = [
    path('subscribe-user', subscribe_user),
    path('attach-payment-method', add_payment_card),
    path('unsubscribe-user', unsubscribe_user),
] 