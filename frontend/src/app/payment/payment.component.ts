import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { SharedService } from '../services/shared.service';
import { ServerService } from '../services/server.service';
declare const Stripe: any;

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.css'],
})
export class PaymentComponent implements OnInit {
  constructor(private shared: SharedService, private server: ServerService) {}
  ngOnInit(): void {
    this.plans_colors = this.shared.plans_colors;
    this.shared.user_data_subject.subscribe((res: any) => {
      this.user_details = res;
      this.stripe = Stripe(res.stripe_public);
    });
  }
  user_details: any;
  show_card_creation: boolean = false;
  creation_in_progress: boolean = false;
  subscription_in_progress: boolean = false;
  cancel_in_progress: boolean = false;
  plan_to_subscribe: any;
  card_element: any;
  sub_annually: boolean = true;
  total_price: number = 0;

  stripe: any;

  plans_colors: any = {};
  plans = [
    {
      name: 'free',
      price_monthly: 0,
      features: [
        { value: '5 monitors', included: true },
        { value: '5 minutes between checks', included: true },
        { value: '1 monitor page', included: true },
        { value: '1 alert email', included: true },
        { value: 'no extra seats', included: false },
      ],
      show_subscribe: false,
    },
    {
      name: 'pro',
      price_monthly: 6,
      price_annually: 5,
      features: [
        { value: '50 monitors', included: true },
        { value: '1 minute between checks', included: true },
        { value: '5 monitor pages', included: true },
        { value: '3 alert emails', included: true },
        { value: 'no extra seats', included: false },
      ],
      show_subscribe: true,
    },
    {
      name: 'business',
      price_monthly: 19,
      price_annually: 15,
      features: [
        { value: '100 monitors', included: true },
        { value: '30 seconds between checks', included: true },
        { value: '10 monitor pages', included: true },
        { value: '10 alert emails', included: true },
        { value: '3 extra seats', included: true },
      ],
      show_subscribe: true,
    },
  ];
  mount_card() {
    if (!this.card_element) {
      const elements = this.stripe.elements();
      const cardElement = elements.create('card');
      this.card_element = cardElement;
      cardElement.mount('.card_element');
    }
  }
  create_payment_method(form: NgForm) {
    if (form.valid) {
      this.creation_in_progress = true;
      this.stripe
        .createPaymentMethod({
          type: 'card',
          card: this.card_element,
          billing_details: {
            name: form.value.name,
          },
        })
        .then((res: any) => {
          if (res.paymentMethod) {
            const data = {
              pm: res.paymentMethod.id,
            };
            this.server.add_payment_card(data).subscribe((res) => {
              if (res.status && res.status == 200) {
                this.shared.refresh_user_data();
                this.shared.show_alert('Card added successfully', 'success');
                this.shared.show_hide_element('monitor_creation');
                this.subscribe_user();
                this.creation_in_progress = false;
              }
            });
          } else if (res.error) {
            this.shared.show_alert(res.error.message, 'alert');
          }
        });
    }
  }
  show_creation_window(plan: string) {
    this.plan_to_subscribe = this.plans.find(
      (plan_) => plan_.name.toLowerCase() == plan
    );
    this.total_price = this.sub_annually
      ? this.plan_to_subscribe.price_annually * 12
      : this.plan_to_subscribe.price_monthly;
    if (this.user_details.payment_card) {
      this.subscribe_user();
    } else {
      this.show_card_creation = true;
      this.shared.show_hide_element('monitor_creation');
      setTimeout(() => {
        this.mount_card();
      }, 300);
    }
  }
  subscribe_user() {
    this.show_card_creation = false;
    this.shared.show_hide_element('monitor_creation');
  }
  confirm_subscribe() {
    if (!this.subscription_in_progress) {
      this.subscription_in_progress = true;
      const data = {
        plan_name: this.plan_to_subscribe.name,
        plan_period: this.sub_annually ? 'annually' : 'monthly',
      };
      this.server.subscribe_user(data).subscribe((res) => {
        if (res.status && res.status == 200) {
          if (res.secure_3D) {
            console.log(res);
            this.stripe
              .confirmCardPayment(res.payment_intent.client_secret, {
                payment_method: res.payment_method,
              })
              .then((result: any) => {
                if (result.error) {
                  this.shared.show_alert(result.error.message, 'alert');
                } else {
                  this.shared.show_alert(
                    `Subscribed to ${data.plan_name} ${data.plan_period} successfully`,
                    'success'
                  );
                  this.subscription_in_progress = false;
                  this.shared.show_hide_element('monitor_creation');
                }
              });
          } else {
            this.shared.show_alert(
              `Subscribed to ${data.plan_name} ${data.plan_period} successfully`
            );
            this.shared.show_hide_element('monitor_creation');
            this.subscription_in_progress = false;
            this.shared.refresh_user_data();
          }
        }
      });
    }
  }
  unsubscribe_user() {
    if (!this.cancel_in_progress) {
      this.cancel_in_progress = true;
      this.server.unsubscribe_user().subscribe((res) => {
        if (res.status && res.status == 200) {
          this.shared.show_alert('Unsubscribed successfully', 'success');
          this.shared.refresh_user_data();
          this.cancel_in_progress = false;
        }
      });
    }
  }
  change_sub() {
    this.sub_annually = !this.sub_annually;
  }
}
