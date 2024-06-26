import { Component, OnInit, Input } from '@angular/core';
import { SharedService } from 'src/app/services/shared.service';
import { ServerService } from 'src/app/services/server.service';
import { animations } from 'src/app/animations';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  animations: animations,
})
export class HeaderComponent implements OnInit {
  @Input() title_: string = 'dashboard';
  @Input() icon: string = 'fa-home';
  constructor(private shared: SharedService, private server: ServerService) {}

  ngOnInit(): void {
    this.plans_colors = this.shared.plans_colors;
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
    this.refresh_notifications();
    this.shared.user_data_subject.subscribe((res) => {
      this.user_details = res;
    });
    this.shared.dark_mode_subject.subscribe((res) => {
      this.dark_mode = res;
    });
    if (localStorage.getItem('dark_mode')) {
      this.dark_mode = true;
    }
    this.shared.emit_user_data();
  }

  plans_colors: any = {};
  shown_popups: any = {};
  all_notifications_seen = true;
  dark_mode: boolean = false;
  notifications: any[] = [];
  user_details: any;
  show_hide_element(elem: string) {
    this.shared.show_hide_element(elem);
    if (!this.all_notifications_seen) {
      this.server
        .see_all_notifications({
          ids: this.notifications.map((notif) => notif.id),
        })
        .subscribe();
      this.all_notifications_seen = true;
      setTimeout(() => {
        this.notifications.forEach((notif) => {
          notif.seen = true;
        });
      }, 1000);
    }
  }

  refresh_notifications() {
    this.server.get_notifications().subscribe((res) => {
      if (res.status == 200) {
        this.notifications = res.notifications;
        for (let notification of res.notifications) {
          if (!notification.seen) {
            this.all_notifications_seen = false;
            break;
          }
        }
      }
    });
  }

  delete_all_notifications() {
    this.server
      .delete_notifications({
        body: { ids: this.notifications.map((notif) => notif.id) },
      })
      .subscribe((res) => {
        if (res.status && res.status == 200) {
          this.show_hide_element('header_notification_popup');
          this.notifications = [];
        }
      });
  }

  enable_dark() {
    if (this.dark_mode) {
      this.shared.disable_dark_mode();
      localStorage.removeItem('dark_mode');
    } else {
      this.shared.enable_dark_mode();
      localStorage.setItem('dark_mode', 'true');
    }
  }
}
