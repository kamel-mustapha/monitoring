import { Component, OnInit, isDevMode } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  constructor(private http: HttpClient) {}
  ngOnInit(): void {
    this.load_monitors();
    const page_icon_container: any = document.getElementById('monitor_icon');
    const page_link_container: any = document.getElementById('monitor_link');
    const page_name_container: any = document.getElementById('monitor_name');
    this.page_icon = page_icon_container.dataset.id;
    this.page_link = page_link_container.dataset.id;
    this.page_name = page_name_container.dataset.id;
    this.check_monitors();
    setInterval(() => {
      this.check_monitors();
    }, 1000);
  }
  loading: boolean = true;
  response_active: boolean = false;
  timings: any = { week: true };
  page_name: string = '';
  page_icon: string = '';
  page_link: string = '';
  monitor_time: number = 90;
  monitors: any = [];
  monitor_down: boolean = false;
  checks_counter = 60;
  change_mode(mode: number) {
    if (mode == 0) {
      this.response_active = true;
    } else {
      this.response_active = false;
    }
  }
  change_timing(timing: string) {
    this.timings = {};
    this.timings[timing] = true;
  }
  check_monitors() {
    this.checks_counter -= 1;
    if (this.checks_counter == 0) {
      this.checks_counter = 60;
      this.load_monitors();
    }
  }
  detect_monitor_down() {
    for (let monitor of this.monitors) {
      if (monitor.down) {
        this.monitor_down = true;
        return;
      }
    }
    this.monitor_down = false;
  }
  load_monitors() {
    const monitor_container: any =
      document.getElementById('monitor_id')?.dataset.id;
    const monitor_id: number = parseInt(monitor_container);
    const api_url = isDevMode()
      ? `http://localhost:8000/api/monitor-page-stats?id=${monitor_id}`
      : `/api/monitor-page-stats?id=${monitor_id}`;
    this.http.get<any>(api_url).subscribe((res) => {
      if (res.status && res.status == 200) {
        this.monitors = res.monitors;
        if (window.innerWidth < 640) {
          this.monitor_time = 30;
          this.monitors.forEach((monitor: any) => {
            monitor.responses = monitor.responses.slice(-30);
            monitor.uptimes = monitor.uptimes.slice(-30);
          });
        } else if (window.innerWidth >= 640 && window.innerWidth <= 1024) {
          this.monitor_time = 60;
          this.monitors.forEach((monitor: any) => {
            monitor.responses = monitor.responses.slice(-60);
            monitor.uptimes = monitor.uptimes.slice(-60);
          });
        }
      }
      this.detect_monitor_down();
      this.loading = false;
    });
  }
  paused_monitors() {
    return this.monitors.filter((m: any) => m.paused == true).length;
  }
  up_monitors() {
    return this.monitors.filter((m: any) => m.down == false).length;
  }
  down_monitors() {
    return this.monitors.filter((m: any) => m.down == true).length;
  }
}
