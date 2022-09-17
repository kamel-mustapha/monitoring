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
      name: 'Light',
      premium: false,
      selected: true,
    },
    {
      name: 'Black',
      premium: false,
      selected: false,
    },
    {
      name: 'Total sense',
      premium: true,
      selected: false,
    },
    {
      name: 'Red shift',
      premium: true,
      selected: false,
    },
  ];
}
