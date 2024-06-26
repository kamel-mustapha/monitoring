import { Component, OnInit, isDevMode } from '@angular/core';
import { Router } from '@angular/router';
import { animations } from './animations';
import { ServerService } from './services/server.service';
import { SharedService } from './services/shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: animations,
})
export class AppComponent implements OnInit {
  constructor(
    private router: Router,
    private shared: SharedService,
    private server: ServerService
  ) {}
  dark_mode: boolean = false;
  ngOnInit(): void {
    if (!isDevMode()) {
      this.server.set_api(this.get_api_key(), '/');
    }

    this.shared.show_popup_subject.subscribe((value) => {
      this.is_alert = value;
    });
    this.shared.message_popup_subject.subscribe((value) => {
      this.popup_message = value;
    });
    this.shared.types_popup_subject.subscribe((value) => {
      this.popup_alert = value;
    });

    this.shared.refresh_user_data();
    this.shared.dark_mode_subject.subscribe((res) => {
      this.dark_mode = res;
    });
    if (localStorage.getItem('dark_mode')) {
      this.shared.enable_dark_mode();
    }
  }
  get_api_key(): string {
    let api_key: string = '';
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      if (cookie.includes('API_KEY')) {
        api_key = cookie.split('=')[1].trim();
      }
    }
    return api_key;
  }
  is_alert: boolean = false;
  popup_alert: any;
  popup_message: string = '';
  hide_popup() {
    this.shared.hide_popup();
  }
}
