import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { isDevMode } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  constructor(private http: HttpClient) {}
  ngOnInit(): void {
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
    const monitor_container: any =
      document.getElementById('monitor_id')?.dataset.id;
    const monitor_id: number = parseInt(monitor_container);
    const api_url = isDevMode()
      ? `http://localhost:8000/api/monitor-page-stats?id=${monitor_id}`
      : `/api/monitor-page-stats?id=${monitor_id}`;
    this.http.get<any>(api_url).subscribe((res) => {
      if (res.status && res.status == 200) {
        this.monitors = res.monitors;
      }
      this.loading = false;
    });

    const page_title_container: any = document.getElementById('monitor_title');
    const page_icon_container: any = document.getElementById('monitor_icon');
    const page_link_container: any = document.getElementById('monitor_link');
    this.page_title = page_title_container.dataset.id;
    this.page_icon = page_icon_container.dataset.id;
    this.page_link = page_link_container.dataset.id;
  }
  loading: boolean = true;
  response_active: boolean = false;
  timings: any = { week: true };
  page_title: string = 'Monitoring page';
  page_icon: string = '';
  page_link: string = '';
  monitor_time: number = 90;
  monitors: any = [];
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
}
