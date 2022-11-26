import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SharedService {
  constructor() {}

  creation_modes: any = {
    monitor_creation: false,
  };

  creation_modes_subject = new Subject<object>();
  show_creation_subject = new Subject<boolean>();

  turn_on_creation(mode: any) {
    this.creation_modes[mode] = true;
    this.emit_creation_modes();
    this.show_creation_subject.next(true);
  }

  turn_off_creation() {
    this.show_creation_subject.next(false);
    this.reset_creation_modes();
    this.emit_creation_modes();
  }

  reset_creation_modes() {
    for (let i in this.creation_modes) {
      this.creation_modes[i] = false;
    }
  }

  emit_creation_modes() {
    this.creation_modes_subject.next(this.creation_modes);
  }
}
