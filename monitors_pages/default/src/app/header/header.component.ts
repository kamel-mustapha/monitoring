import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}
  @Input() page_icon: string = '';
  @Input() page_link: string = '';
  @Input() page_name: string = '';
  @Input() monitor_down: boolean = false;
  @Input() checks_counter: number = 60;
  @Input() loading: boolean = false;
}
