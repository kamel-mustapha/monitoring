import { Component, OnInit } from '@angular/core';
import { ServerService } from 'src/app/services/server.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent implements OnInit {
  constructor(private server: ServerService) {}

  ngOnInit(): void {
    this.server.get_user_details().subscribe((res) => {
      this.user_details = res.user;
    });
  }
  user_details: any;
}
