import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { ServerService } from './server.service';

@Injectable({
  providedIn: 'root',
})
export class SharedService {
  constructor(private server: ServerService) {}
  plans_colors: any = {
    free: '#22c55e',
    pro: '#3730a3',
    business: '#86198f',
  };
  // toast
  types_popup: any = {
    success: false,
    info: false,
    alert: false,
    alarm: false,
  };
  types_popup_subject = new Subject<object>();
  show_popup_subject = new Subject<boolean>();
  message_popup_subject = new Subject<string>();

  show_alert(
    message: string,
    type: string = 'success',
    duration: number = 10000
  ) {
    this.reset_popup();
    this.types_popup[type] = true;
    this.message_popup_subject.next(message);
    this.types_popup_subject.next(this.types_popup);
    this.show_popup_subject.next(true);
    setTimeout(() => {
      this.hide_popup();
      this.reset_popup();
    }, duration);
  }

  reset_popup() {
    this.message_popup_subject.next('');
    for (let i in this.types_popup) {
      this.types_popup[i] = false;
    }
    this.types_popup_subject.next(this.types_popup);
  }

  hide_popup() {
    this.show_popup_subject.next(false);
  }

  // popups
  shown_popups: any = {};
  shown_popups_subject = new Subject<any>();

  add_to_popups(elem: any) {
    this.shown_popups = {};
    this.shown_popups[elem] = true;
    this.shown_popups_subject.next(this.shown_popups);
  }

  reset_all_popups() {
    this.shown_popups = {};
    this.shown_popups_subject.next(this.shown_popups);
  }

  show_hide_element(elem: string) {
    if (this.shown_popups[elem]) {
      this.reset_all_popups();
    } else {
      this.add_to_popups(elem);
    }
  }
  user_data: any;
  user_data_subject = new Subject();
  refresh_user_data() {
    this.server.get_user_details().subscribe((res) => {
      if (res.status && res.status == 200) {
        this.user_data = res.user;
        this.user_data_subject.next(this.user_data);
      }
    });
  }
  emit_user_data() {
    this.user_data_subject.next(this.user_data);
  }
}
