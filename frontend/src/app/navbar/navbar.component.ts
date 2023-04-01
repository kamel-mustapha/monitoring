import { Component, OnInit } from '@angular/core';
import { SharedService } from '../services/shared.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  constructor(private shared: SharedService) {}
  ngOnInit(): void {
    this.shared.user_data_subject.subscribe((res) => {
      this.user_details = res;
    });
  }
  user_details: any;
  navbar_links = [
    {
      link: '/home',
      icon: 'fas fa-home',
      name: 'home',
    },
    {
      link: '/pages',
      icon: 'fas fa-file-alt',
      name: 'pages',
    },
    {
      link: '/profile',
      icon: 'fas fa-user',
      name: 'profile',
    },
  ];
  navbar_secondary_links: any[] = [
    {
      link: '/plans',
      icon: 'fas fa-money-check-alt',
      name: 'plans',
    },
  ];
  animate_logo: boolean = false;
  large_navbar: boolean = false;
  logo_animation() {
    this.animate_logo = !this.animate_logo;
  }
}
