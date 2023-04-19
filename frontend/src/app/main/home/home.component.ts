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
    this.get_monitors(true);
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
    this.shared.user_data_subject.subscribe((res: any) => {
      this.user_data = res;
    });
    this.shared.user_data_subject.subscribe((res: any) => {
      this.user_details = res;
    });
  }

  monitor_edit_loading: any = {};
  user_details: any;
  monitors: any[] = [];
  monitor_to_edit: any;
  alert_emails: string[] = [];
  shown_popups: any = {};
  loading_monitors: boolean = true;
  loading_events: boolean = true;
  selected_monitor: string = 'Select a monitor';
  monitor_selected: boolean = false;
  events: any[] = [];
  creation_modes: any;
  creation_in_progress: boolean = false;
  create_word: string = 'Create';
  user_data: any = {};
  monitor_creation_defaults: any = {};
  monitor_form_validation: any = {
    name: false,
    type: false,
    link: false,
  };

  build_monitor_creation_default() {
    this.create_word = 'Create';
    this.monitor_creation_defaults = {
      name: '',
      link: '',
      interval: this.user_details.min_interval,
      success: 200,
      timeout: 30,
    };
    this.alert_emails = [this.user_data.email];
    for (let i in this.monitor_form_validation) {
      this.monitor_form_validation[i] = false;
    }
  }
  get_monitors(init = false) {
    this.server.get_monitors().subscribe((value) => {
      if (value.monitors) {
        this.monitors = value.monitors;
      }
      if (init && this.monitors.length > 0) {
        try {
          this.select_monitor(this.monitors[0].id);
        } catch (e) {}
      } else {
        this.loading_events = false;
      }
      this.loading_monitors = false;
    });
  }

  show_creation_window(edit = false, monitor_id = null) {
    if (edit) {
      this.create_word = 'Edit';
      this.monitor_to_edit = this.monitors.find(
        (monitor) => monitor.id == monitor_id
      );
      this.alert_emails = this.monitor_to_edit.alert_emails.map(
        (email: any) => email.email
      );
      this.monitor_creation_defaults.interval = this.monitor_to_edit.interval;
      this.monitor_creation_defaults.link = this.monitor_to_edit.link;
      this.monitor_creation_defaults.name = this.monitor_to_edit.name;
      this.monitor_creation_defaults.success =
        this.monitor_to_edit.success_status;
      this.monitor_creation_defaults.timeout = this.monitor_to_edit.timeout;
    } else {
      this.build_monitor_creation_default();
    }
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
      this.loading_events = false;
      this.monitor_selected = true;
      this.shared.reset_all_popups();
    });
  }

  delete_monitor(id: number) {
    this.monitor_edit_loading[id] = true;
    this.server.delete_monitor({ body: { monitor: id } }).subscribe(
      (res) => {
        if (res && res.status && res.status == 200) {
          this.monitor_edit_loading = {};
          this.shared.reset_all_popups();
          this.shared.show_alert('Monitor deleted successfully');
          this.monitors = this.monitors.filter((monitor) => monitor.id != id);
          this.monitor_selected = false;
          this.selected_monitor = 'Select a monitor';
        }
      },
      (error) => {
        this.shared.show_alert(error.statusText, 'alert');
      }
    );
  }
  pause_monitor(id: number) {
    this.monitor_edit_loading[id] = true;
    this.server.pause_monitor(id).subscribe(
      (res) => {
        if (res && res.status && res.status == 200) {
          this.monitor_edit_loading = {};
          this.shared.reset_all_popups();
          this.shared.show_alert('Monitor paused successfully');
        }
        this.get_monitors();
      },
      (error) => {
        this.shared.show_alert(error.statusText, 'alert');
      }
    );
  }
  start_monitor(id: number) {
    this.monitor_edit_loading[id] = true;
    this.server.start_monitor(id).subscribe(
      (res) => {
        if (res && res.status && res.status == 200) {
          this.monitor_edit_loading = {};
          this.shared.reset_all_popups();
          this.shared.show_alert('Monitor started successfully');
          this.get_monitors();
        } else if (res.message) {
          this.shared.show_alert(res.message, 'alert');
        }
      },
      (error) => {
        this.shared.show_alert(error.statusText, 'alert');
      }
    );
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
      form.value.alert_emails = this.alert_emails.slice(
        0,
        this.user_data.max_alert_emails
      );
      if (this.create_word == 'Create') {
        this.server.create_monitor(form.value).subscribe(
          (response) => {
            if (
              response &&
              response.status == 200 &&
              response.message == 'success'
            ) {
              this.shared.show_alert('Monitor created successfully');
              this.show_creation_window();
              this.get_monitors();
              this.shared.refresh_user_data();
              this.build_monitor_creation_default();
            } else if (
              response &&
              response.status == 200 &&
              response.message != 'success'
            ) {
              this.shared.show_alert(response.message, 'alert');
            }
            this.creation_in_progress = false;
          },
          (error) => {
            this.shared.show_alert(error.statusText, 'alarm');
            this.creation_in_progress = false;
          }
        );
      } else {
        form.value.monitor = this.monitor_to_edit.id;
        this.server.update_monitor(form.value).subscribe((response) => {
          if (response && response.status == 200) {
            this.shared.show_alert('Monitor updated successfully');
            this.show_creation_window();
            this.get_monitors();
            this.shared.refresh_user_data();
            this.build_monitor_creation_default();
          } else if (response.message) {
            this.shared.show_alert(response.message, 'alert');
          }
          this.creation_in_progress = false;
        });
      }
    } else {
      for (let i in form.value) {
        if (form.value[i].length == 0) {
          this.monitor_form_validation[i] = true;
        }
      }
    }
  }
  remove_alert_email(email: string) {
    if (this.alert_emails.length > 1) {
      this.alert_emails = this.alert_emails.filter((mail) => mail != email);
    } else {
      this.shared.show_alert('At least one email should be included', 'alert');
    }
  }
  add_alert_email(email: string) {
    if (this.alert_emails.includes(email.toLocaleLowerCase())) {
      this.shared.show_alert('Email already in the list', 'alert');
    } else {
      if (this.alert_email_input.length == this.user_data.max_alert_emails) {
        this.shared.show_alert('Upgrade to get more alert emails', 'alert');
        return;
      }
      this.alert_emails.push(email.toLocaleLowerCase());
    }
  }
  alert_email_input(event: any) {
    if (event.which == 32) {
      if (
        /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
          event.target.value.trim()
        )
      ) {
        this.add_alert_email(event.target.value);
        event.target.value = '';
      } else {
        this.shared.show_alert('Invalid email', 'alert');
      }
    }
  }
}
