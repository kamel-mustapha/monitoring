import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { SharedService } from 'src/app/services/shared.service';
import { ServerService } from 'src/app/services/server.service';
import { animations } from 'src/app/animations';

@Component({
  selector: 'app-pages',
  templateUrl: './pages.component.html',
  styleUrls: ['./pages.component.css'],
  animations: animations,
})
export class PagesComponent implements OnInit {
  constructor(private shared: SharedService, private server: ServerService) {}

  ngOnInit(): void {
    this.shared.shown_popups_subject.subscribe((value) => {
      this.shown_popups = value;
    });
  }
  all_pages_selected: boolean = false;
  one_page_selected: boolean = false;
  shown_popups: any = {};
  pages: any[] = [
    {
      id: 1,
      name: 'Default Light',
      premium: false,
      selected: false,
      owned: true,
      monitors_nb: 10,
      link: 'https://google.com',
      seen: 5,
    },
    {
      id: 2,
      name: 'Default Black',
      premium: false,
      selected: false,
      owned: true,
      monitors_nb: 10,
      link: 'https://google.com',
      seen: 5,
    },
    {
      id: 3,
      name: 'Total sense',
      premium: true,
      selected: false,
      owned: false,
      price: 5.99,
      monitors_nb: 10,
      link: 'https://google.com',
      seen: 5,
    },
    {
      id: 4,
      name: 'Red shift',
      premium: true,
      selected: false,
      owned: false,
      price: 5.99,
      monitors_nb: 10,
      link: 'https://google.com',
      seen: 5,
    },
  ];
  monitor_form_validation: any = {
    name: false,
    type: false,
    link: false,
  };
  creation_in_progress: boolean = false;
  page_creations_modes = {
    page: true,
    monitors: false,
  };
  select_all_pages() {
    this.all_pages_selected = !this.all_pages_selected;
    if (this.all_pages_selected) {
      this.pages.forEach((page) => (page.selected = true));
      this.one_page_selected = false;
    } else {
      this.pages.forEach((page) => (page.selected = false));
    }
  }

  select_page(page_index: number) {
    this.pages[page_index].selected = !this.pages[page_index].selected;
    let selected_pages = this.pages.filter((page) => page.selected);
    if (selected_pages.length > 1 || selected_pages.length < 1) {
      this.one_page_selected = false;
    } else if ((selected_pages.length = 1)) {
      this.one_page_selected = true;
    }
  }

  show_creation_window() {
    this.shared.show_hide_element('monitor_creation');
  }

  submit_page(form: NgForm, step: number) {
    if (step == 0) {
      this.page_creations_modes['page'] = false;
      this.page_creations_modes['monitors'] = true;
    }
  }
}
