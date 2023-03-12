import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ServerService {
  constructor(private server: HttpClient) {}
  api_key: string = '417fe54b852719f87777f44f2a283e14';
  api_link: string = 'http://localhost:8000/';

  set_api(key: string, link: string) {
    this.api_key = key;
    this.api_link = link;
  }

  get_monitors() {
    return this.server.get<any>(
      `${this.api_link}api/monitor?key=${this.api_key}`
    );
  }
  create_monitor(monitor: {}) {
    return this.server.post<any>(
      `${this.api_link}api/monitor?key=${this.api_key}`,
      monitor
    );
  }

  delete_monitor(monitor: {}) {
    return this.server.delete<any>(
      `${this.api_link}api/monitor?key=${this.api_key}`,
      monitor
    );
  }

  pause_monitor(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}api/pause-monitor?key=${this.api_key}&monitor=${monitor}`
    );
  }

  start_monitor(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}api/start-monitor?key=${this.api_key}&monitor=${monitor}`
    );
  }

  get_events(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}api/event?key=${this.api_key}&monitor=${monitor}`
    );
  }

  get_notifications() {
    return this.server.get<any>(
      `${this.api_link}api/notification?key=${this.api_key}`
    );
  }

  see_all_notifications(data: {}) {
    return this.server.put<any>(
      `${this.api_link}api/notification?key=${this.api_key}`,
      data
    );
  }

  delete_notifications(data: {}) {
    return this.server.delete<any>(
      `${this.api_link}api/notification?key=${this.api_key}`,
      data
    );
  }

  get_pages() {
    return this.server.get<any>(`${this.api_link}api/get-pages`);
  }

  create_user_page(data: any) {
    return this.server.post<any>(
      `${this.api_link}api/user-pages?key=${this.api_key}`,
      data
    );
  }

  get_user_pages() {
    return this.server.get<any>(
      `${this.api_link}api/user-pages?key=${this.api_key}`
    );
  }

  delete_user_page(data: any) {
    return this.server.delete<any>(
      `${this.api_link}api/user-pages?key=${this.api_key}`,
      data
    );
  }

  get_user_details() {
    return this.server.get<any>(
      `${this.api_link}api/get-user-details?key=${this.api_key}`
    );
  }

  update_monitor(monitor: {}) {
    return this.server.put<any>(
      `${this.api_link}api/monitor?key=${this.api_key}`,
      monitor
    );
  }

  add_payment_card(data: {}) {
    return this.server.post<any>(
      `${this.api_link}payment/attach-payment-method?key=${this.api_key}`,
      data
    );
  }

  subscribe_user(data: {}) {
    return this.server.post<any>(
      `${this.api_link}payment/subscribe-user?key=${this.api_key}`,
      data
    );
  }

  unsubscribe_user() {
    return this.server.get<any>(
      `${this.api_link}payment/unsubscribe-user?key=${this.api_key}`
    );
  }
}
