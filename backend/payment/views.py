import json
from django.shortcuts import render
from django.http import JsonResponse
from payment.common import *
from payment.models import Plan
from django.views.decorators.csrf import csrf_exempt



from logging import getLogger
logger = getLogger(__name__)

@csrf_exempt
def subscribe_user(req):
    try:
        data = json.loads(req.body)
        plan_name = data.get("plan_name")
        plan_period = data.get("plan_period")
        if plan_name and plan_period:
            plan = Plan.objects.get(name=plan_name.title(), period=plan_period)
            secure_3d, subscription = attach_subscription(plan, req.user)
            if secure_3d:
                last_invoice = retrieve_invoice(subscription.get("latest_invoice"))
                req.res["secure_3D"] = True
                req.res["message"] = "3D secure required"
                req.res["payment_intent"] = retrieve_payment_intent(last_invoice.get("payment_intent"))
                req.res["payment_method"] = req.user.payment_method
            else:
                req.user.sub = plan.name
                req.user.period = plan.period
                req.user.save()
                req.res["message"] = "subscription created"
            req.res["status"] = 200
    except Exception as e:
        logger.exception(e)
    return JsonResponse(req.res, status=req.res["status"])

@csrf_exempt
def add_payment_card(req):
    try:
        data = json.loads(req.body)
        pm = data.get("pm")
        if pm:
            if not req.user.stripe_id:
                customer = create_customer(req.user)
            if not req.user.payment_method:
                pm = attach_payment_method(pm, req.user)
            req.res["status"] = 200
            req.res["message"] = "success"
    except Exception as e:
        logger.exception(e)
    return JsonResponse(req.res, status=req.res["status"])


def unsubscribe_user(req):
    try:
        detach_subscription(req.user)
        req.user.sub = "Free"
        req.user.period = "monthly"
        req.user.save()
        req.res["status"] = 200
        req.res["message"] = "success"
    except Exception as e:
        logger.exception(e)
    return JsonResponse(req.res, status=req.res["status"])