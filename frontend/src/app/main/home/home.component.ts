import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../services/shared.service';
import { ServerService } from 'src/app/services/server.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  constructor(private shared: SharedService, private server: ServerService) {}

  ngOnInit(): void {
    this.get_monitors();
  }

  monitors: any[] = [];

  show_monitor_creation() {
    this.shared.turn_on_creation('monitor_creation');
  }

  hide_monitor_creation() {
    this.shared.turn_off_creation();
  }

  get_monitors() {
    this.server.get_monitors().subscribe((value) => {
      this.monitors = value.monitors;
    });
  }
}
