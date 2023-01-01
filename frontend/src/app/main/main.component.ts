import { Component, OnInit, HostListener } from '@angular/core';
import { NgForm } from '@angular/forms';
import { animations } from '../animations';
import { SharedService } from '../services/shared.service';
import { ServerService } from '../services/server.service';
import { HomeComponent } from './home/home.component';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
  animations: animations,
})
export class MainComponent implements OnInit {
  constructor(
    private shared: SharedService,
    private server: ServerService,
    private home: HomeComponent
  ) {}

  ngOnInit(): void {
    this.shared.shown_popups_subject.subscribe((show_creation) => {
      this.shown_popups = show_creation;
    });
    // temporary
    // this.shared.turn_on_creation('monitor_creation');
  }

  shown_popups: any = {};

  @HostListener('document:keydown.escape')
  hide_creation_window() {
    this.shared.reset_all_popups();
  }
}
