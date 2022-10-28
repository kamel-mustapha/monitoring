import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pages',
  templateUrl: './pages.component.html',
  styleUrls: ['./pages.component.css'],
})
export class PagesComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  pages = [
    {
      name: 'Default Light',
      premium: false,
      selected: true,
      owned: true,
    },
    {
      name: 'Default Black',
      premium: false,
      selected: false,
      owned: true,
    },
    {
      name: 'Total sense',
      premium: true,
      selected: false,
      owned: false,
      price: 5.99,
    },
    {
      name: 'Red shift',
      premium: true,
      selected: false,
      owned: false,
      price: 5.99,
    },
  ];
}
