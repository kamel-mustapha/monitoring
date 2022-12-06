import { Component, OnInit, Input } from '@angular/core';
import { SharedService } from 'src/app/services/shared.service';
import { animations } from 'src/app/animations';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
  animations: animations,
})
export class HeaderComponent implements OnInit {
  @Input() title: string = 'home';
  @Input() icon: string = 'fa-home';
  constructor(private shared: SharedService) {}

  ngOnInit(): void {
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
  }
  shown_popups: any = {};
  show_hide_element(elem: string) {
    this.shared.show_hide_element(elem);
    console.log(this.shown_popups);
  }
}
