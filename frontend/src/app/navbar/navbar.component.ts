import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  constructor() {}
  ngOnInit(): void {}
  navbar_links = [
    {
      link: '/home',
      icon: 'fas fa-home',
      name: 'home',
    },
    {
      link: '/pages',
      icon: 'fas fa-file-code',
      name: 'pages',
    },
    {
      link: '/profile',
      icon: 'fas fa-user',
      name: 'profile',
    },
    // {
    //   link: '/settings',
    //   icon: 'fas fa-cog',
    // },
  ];
  animate_logo: boolean = false;

  logo_animation() {
    console.log('s');
    this.animate_logo = !this.animate_logo;
  }
}
