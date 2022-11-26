import { Component, OnInit, HostListener } from '@angular/core';
import { animations } from '../animations';
import { SharedService } from '../services/shared.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
  animations: animations,
})
export class MainComponent implements OnInit {
  constructor(private shared: SharedService) {}

  ngOnInit(): void {
    this.shared.creation_modes_subject.subscribe((modes) => {
      this.creation_modes = modes;
    });
    this.shared.show_creation_subject.subscribe((show_creation) => {
      this.show_creation = show_creation;
    });
    // temporary
    // this.shared.turn_on_creation('monitor_creation');
  }

  show_creation: boolean = false;
  creation_modes: any;

  @HostListener('document:keydown.escape')
  hide_creation_window() {
    this.shared.turn_off_creation();
  }
}
