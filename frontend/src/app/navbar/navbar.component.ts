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
    this.shared.dark_mode_subject.subscribe((res) => {
      this.dark_mode = res;
    });
    if (localStorage.getItem('dark_mode')) {
      this.shared.enable_dark_mode();
    }
    this.shared.user_data_subject.subscribe((res) => {
      this.user_details = res;
    });
  }
  dark_mode: boolean = false;
  user_details: any;
  navbar_links = [
    {
      link: '/dashboard',
      icon: 'fas fa-home',
      name: 'dashboard',
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
