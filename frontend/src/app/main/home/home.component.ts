import { Component, OnInit } from '@angular/core';
import { SharedService } from '../../services/shared.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  constructor(private shared: SharedService) {}

  ngOnInit(): void {}

  monitors: any[] = [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6];

  show_monitor_creation() {
    this.shared.turn_on_creation('monitor_creation');
  }

  hide_monitor_creation() {
    this.shared.turn_off_creation();
  }
}
