import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { animations } from './animations';
import { SharedService } from './services/shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: animations,
})
export class AppComponent implements OnInit {
  constructor(private router: Router, private shared: SharedService) {}
  ngOnInit(): void {
    this.router.navigate(['home']);
    this.shared.show_popup_subject.subscribe((value) => {
      this.is_alert = value;
    });
    this.shared.message_popup_subject.subscribe((value) => {
      this.popup_message = value;
    });
    this.shared.types_popup_subject.subscribe((value) => {
      this.popup_alert = value;
    });
  }

  is_alert: boolean = false;
  popup_alert: any;
  popup_message: string = '';
  hide_popup() {
    this.shared.hide_popup();
  }
}
