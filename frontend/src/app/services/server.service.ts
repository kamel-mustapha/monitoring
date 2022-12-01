import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ServerService {
  constructor(private server: HttpClient) {}

  get_monitors() {
    return this.server.get<any>(
      'http://127.0.0.1:8000/api/monitor?key=697b2cb949093bfe47017e4aad2d49d4'
    );
  }
  create_monitor(monitor: {}) {
    return this.server.post<any>(
      'http://127.0.0.1:8000/api/monitor?key=697b2cb949093bfe47017e4aad2d49d4',
      monitor
    );
  }
}
