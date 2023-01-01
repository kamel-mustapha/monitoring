import { Component, OnInit } from '@angular/core';
import { SharedService } from '../services/shared.service';
@Component({
  selector: 'app-popup',
  templateUrl: './popup.component.html',
  styleUrls: ['./popup.component.css'],
})
export class PopupComponent implements OnInit {
  constructor(private shared: SharedService) {}

  ngOnInit(): void {
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
  }
  shown_popups: any = {};

  show_creation_window() {
    this.shared.show_hide_element('monitor_creation');
  }
}
