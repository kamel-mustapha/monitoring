import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SharedService {
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
  // monitor creation
  creation_modes: any = {
    monitor_creation: false,
  };
  creation_modes_subject = new Subject<object>();

  turn_on_creation(mode: any) {
    this.creation_modes[mode] = true;
    this.creation_modes_subject.next(this.creation_modes);
    this.show_hide_element('monitor_creation');
  }
  turn_off_creation() {
    this.reset_all_popups();
    this.reset_creation_modes();
    this.creation_modes_subject.next(this.creation_modes);
  }
  reset_creation_modes() {
    for (let i in this.creation_modes) {
      this.creation_modes[i] = false;
    }
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
}
