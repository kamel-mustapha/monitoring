import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { ServerService } from 'src/app/services/server.service';
import { animations } from 'src/app/animations';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  animations: animations,
})
export class HomeComponent implements OnInit {
  constructor(private shared: SharedService, private server: ServerService) {}

  ngOnInit(): void {
    this.get_monitors();
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
  }

  monitors: any[] = [];
  shown_popups: any = {};
  loading_monitors: boolean = true;
  loading_events: boolean = true;
  selected_monitor: string = 'Select a monitor';
  monitor_selected: boolean = false;
  events: any[] = [];
  creation_modes: any;
  creation_in_progress: boolean = false;
  monitor_form_validation: any = {
    name: false,
    type: false,
    link: false,
  };

  get_monitors() {
    this.server.get_monitors().subscribe((value) => {
      if (value.monitors) {
        this.monitors = value.monitors;
      }

      setTimeout(() => {
        this.loading_monitors = false;
        this.loading_events = false;
      }, 500);
    });
  }

  show_creation_window() {
    this.shared.show_hide_element('monitor_creation');
  }

  show_hide_element(elem: string) {
    this.shared.show_hide_element(elem);
  }

  show_campaign_edit(id: number) {
    this.shared.show_hide_element(`campaign_edit_element_${id}`);
  }

  select_monitor(id: number) {
    this.loading_events = true;
    let monitor = this.monitors.find((elem) => elem.id == id);
    this.server.get_events(id).subscribe((res) => {
      if (res && res.status && res.status == 200) {
        this.events = res.events;
        this.selected_monitor = monitor.name;
      }
      setTimeout(() => {
        this.loading_events = false;
        this.monitor_selected = true;
      }, 500);
    });
  }

  delete_monitor(id: number) {
    this.server.delete_monitor({ body: { monitor: id } }).subscribe((res) => {
      if (res && res.status && res.status == 200) {
        this.shared.show_alert('Monitor deleted successfully');
        this.monitors = this.monitors.filter((monitor) => monitor.id != id);
        this.monitor_selected = false;
        this.selected_monitor = 'Select a monitor';
      }
    });
  }
  pause_monitor(id: number) {
    this.server.pause_monitor(id).subscribe((res) => {
      if (res && res.status && res.status == 200) {
        this.shared.show_alert('Monitor paused successfully');
      }
      this.get_monitors();
    });
  }
  start_monitor(id: number) {
    this.server.start_monitor(id).subscribe((res) => {
      if (res && res.status && res.status == 200) {
        this.shared.show_alert('Monitor started successfully');
        this.get_monitors();
      }
    });
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
          this.shared.show_alert('Monitor created successfully');
          form.reset();
          this.show_creation_window();
          this.get_monitors();
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
