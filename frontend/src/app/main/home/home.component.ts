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

  get_monitors() {
    this.server.get_monitors().subscribe((value) => {
      this.monitors = value.monitors;
    });
  }

  show_creation_window() {
    this.shared.turn_on_creation('monitor_creation');
  }

  show_hide_element(elem: string) {
    this.shared.show_hide_element(elem);
  }

  show_campaign_edit(id: number) {
    this.shared.add_to_popups(`campaign_edit_element_${id}`);
    console.log(this.shown_popups);
  }
}
