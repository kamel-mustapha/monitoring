import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ServerService {
  constructor(private server: HttpClient) {}
  api_key: string = '417fe54b852719f87777f44f2a283e14';
  api_link: string = 'http://localhost:8000/api/';

  set_api(key: string, link: string) {
    this.api_key = key;
    this.api_link = link;
  }

  get_monitors() {
    return this.server.get<any>(`${this.api_link}monitor?key=${this.api_key}`);
  }
  create_monitor(monitor: {}) {
    return this.server.post<any>(
      `${this.api_link}monitor?key=${this.api_key}`,
      monitor
    );
  }

  delete_monitor(monitor: {}) {
    return this.server.delete<any>(
      `${this.api_link}monitor?key=${this.api_key}`,
      monitor
    );
  }

  pause_monitor(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}pause-monitor?key=${this.api_key}&monitor=${monitor}`
    );
  }

  start_monitor(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}start-monitor?key=${this.api_key}&monitor=${monitor}`
    );
  }

  get_events(monitor: number) {
    return this.server.get<any>(
      `${this.api_link}event?key=${this.api_key}&monitor=${monitor}`
    );
  }

  get_notifications() {
    return this.server.get<any>(
      `http://127.0.0.1:8000/api/notification?key=417fe54b852719f87777f44f2a283e14`
    );
  }

  see_all_notifications(data: {}) {
    return this.server.put<any>(
      `http://127.0.0.1:8000/api/notification?key=417fe54b852719f87777f44f2a283e14`,
      data
    );
  }

  delete_notifications(data: {}) {
    return this.server.delete<any>(
      `http://127.0.0.1:8000/api/notification?key=417fe54b852719f87777f44f2a283e14`,
      data
    );
  }
}
