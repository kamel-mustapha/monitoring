import { Component, OnInit } from '@angular/core';
// import { ServerService } from 'src/app/services/server.service';
import { SharedService } from 'src/app/services/shared.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
})
export class ProfileComponent implements OnInit {
  constructor(private shared: SharedService) {}

  ngOnInit(): void {
    this.shared.user_data_subject.subscribe((res) => {
      this.user_details = res;
    });
  }
  user_details: any;
}
