import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css'],
})
export class NavbarComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}
  animate_logo: boolean = false;
  logo_animation() {
    console.log('s');
    this.animate_logo = !this.animate_logo;
  }
}
