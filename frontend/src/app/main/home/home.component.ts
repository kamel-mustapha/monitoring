import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { ServerService } from 'src/app/services/server.service';
import { animations } from 'src/app/animations';

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
    this.shared.turn_on_creation('monitor_creation');
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
      }
    });
  }
}
