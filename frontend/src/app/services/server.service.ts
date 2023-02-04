import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ServerService {
  constructor(private server: HttpClient) {}

  get_monitors() {
    return this.server.get<any>(
      'http://127.0.0.1:8000/api/monitor?key=417fe54b852719f87777f44f2a283e14'
    );
  }
  create_monitor(monitor: {}) {
    return this.server.post<any>(
      'http://127.0.0.1:8000/api/monitor?key=417fe54b852719f87777f44f2a283e14',
      monitor
    );
  }

  delete_monitor(monitor: {}) {
    return this.server.delete<any>(
      'http://127.0.0.1:8000/api/monitor?key=417fe54b852719f87777f44f2a283e14',
      monitor
    );
  }

  pause_monitor(monitor: number) {
    return this.server.get<any>(
      `http://127.0.0.1:8000/api/pause-monitor?monitor=${monitor}&key=417fe54b852719f87777f44f2a283e14`
    );
  }

  start_monitor(monitor: number) {
    return this.server.get<any>(
      `http://127.0.0.1:8000/api/start-monitor?monitor=${monitor}&key=417fe54b852719f87777f44f2a283e14`
    );
  }

  get_events(monitor: number) {
    return this.server.get<any>(
      `http://127.0.0.1:8000/api/event?monitor=${monitor}&key=417fe54b852719f87777f44f2a283e14`
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
