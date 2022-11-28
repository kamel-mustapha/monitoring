import { Component, OnInit, HostListener } from '@angular/core';
import { NgForm } from '@angular/forms';
import { animations } from '../animations';
import { SharedService } from '../services/shared.service';
import { ServerService } from '../services/server.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
  animations: animations,
})
export class MainComponent implements OnInit {
  constructor(private shared: SharedService, private server: ServerService) {}

  ngOnInit(): void {
    this.shared.creation_modes_subject.subscribe((modes) => {
      this.creation_modes = modes;
    });
    this.shared.show_creation_subject.subscribe((show_creation) => {
      this.show_creation = show_creation;
    });
    // temporary
    this.shared.turn_on_creation('monitor_creation');
  }

  show_creation: boolean = false;
  creation_modes: any;
  creation_in_progress: boolean = false;

  monitor_form_validation: any = {
    name: false,
    type: false,
    link: false,
  };

  @HostListener('document:keydown.escape')
  hide_creation_window() {
    this.shared.turn_off_creation();
  }

  reset_validation() {
    for (let i in this.monitor_form_validation) {
      this.monitor_form_validation[i] = false;
    }
  }

  submit_monitor(form: NgForm) {
    this.reset_validation();
    if (form.valid) {
      this.creation_in_progress = true;
      if (form.value.alert_emails.length > 0) {
        form.value.alert_emails = form.value.alert_emails.split(' ');
      }
      this.server.create_monitor(form.value).subscribe((response) => {
        if (response && response.status == 200) {
          this.shared.turn_off_creation();
          form.reset();
        } else {
          console.log(response);
        }
        this.creation_in_progress = false;
      });
    } else {
      for (let i in form.value) {
        if (form.value[i].length == 0) {
          this.monitor_form_validation[i] = true;
        }
      }
    }
  }
}
