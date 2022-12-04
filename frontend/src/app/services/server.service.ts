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
}
