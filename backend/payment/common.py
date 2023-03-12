import stripe
from payment.models import APIKey


api_key = APIKey.objects.filter(active=True)
if api_key:
    stripe.api_key = api_key[0].private

def create_customer(user:object) -> object:
    customer = stripe.Customer.create(
        email=user.email,
        name=f"{user.first_name} {user.last_name}"
    )
    if customer:
        user.stripe_id = customer.get("id")
        user.save()
        return customer
    
def retrieve_customer(user:object) -> object:
    customer = stripe.Customer.retrieve(user.stripe_id)
    if customer:
        return customer

def delete_customer(user:object) -> object:
    response = stripe.Customer.delete(user.stripe_id)
    if response:
        user.stripe_id = None
        user.save()
        return response

def attach_payment_method(pm:str, user:object) -> object:
    response = stripe.PaymentMethod.attach(
        pm,
        customer = user.stripe_id
    )
    if response:
        stripe.Customer.modify(
            user.stripe_id,
            invoice_settings = {
                'default_payment_method' : pm
            }
        )
        user.payment_method = response.get("id")
        user.card_last_digit = response.get("card").get("last4")
        user.save()
        return response

def detach_payment_method(user:object) -> object:
    response = stripe.PaymentMethod.detach(
        user.payment_method,
    )
    if response:
        user.payment_method = None
        user.card_last_digit = None
        user.save()
        return response

def detach_subscription(user:object) -> object:
    response = stripe.Subscription.delete(
        user.stripe_sub,
    )
    if response:
        user.stripe_sub = None
        user.save()
        return response
    
def attach_subscription(plan:object, user:object) -> object:
    secure_3D = False
    if user.stripe_sub:
        detach_subscription(user)
    response = stripe.Subscription.create(
        customer=user.stripe_id,
        items=[
            {"price": plan.stripe_id},
        ],
        payment_behavior = 'allow_incomplete'
    )
    if response and response.get("status") != "incomplete":
        user.stripe_sub = response.get("id")
        user.save()
        return secure_3D, response
    else:
        secure_3D = True
        return secure_3D, response
    
def retrieve_invoice(invoice: str) -> object:
    response = stripe.Invoice.retrieve(
        invoice,
    )
    if response:
        return response
    
def retrieve_payment_intent(pi: str) -> object:
    response = stripe.PaymentIntent.retrieve(
        pi
    )
    if response:
        return response