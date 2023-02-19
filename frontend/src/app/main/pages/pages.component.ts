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

    this.server.get_monitors().subscribe((res) => {
      if (res.status && res.status == 200) {
        this.monitors = res.monitors;
        this.monitors.forEach((monitor) => (monitor.selected = false));
      }
    });

    this.server.get_pages().subscribe((res) => {
      if (res.status && res.status == 200) {
        this.pages_marketplace = res.pages;
        // for dev
        this.pages_marketplace.forEach(
          (page) => (page.picture = `http://localhost:8000${page.picture}`)
        );
      }
    });
    this.refresh_user_pages();
  }

  all_pages_selected: boolean = false;
  one_page_selected: boolean = false;
  creation_in_progress: boolean = false;
  loading_pages: boolean = true;
  icon_file: any;
  page_creation_active_index: number = 0;
  shown_popups: any = {};

  page_creations_modes: any = {
    page: true,
    monitors: false,
    details: false,
  };

  monitor_form_validation: any = {
    name: false,
    type: false,
    link: false,
  };

  page_creation_forms: any = {
    page: true,
    monitors: false,
    details: false,
  };

  pages: any[] = [];

  pages_marketplace: any[] = [];

  monitors: any[] = [];

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
    this.monitor_form_validation = {};
    if (step == 0) {
      this.activate_page_creation_mode('page');
    } else if (step == 1) {
      this.page_creation_forms['page'] = form.value;
      this.activate_page_creation_mode('monitors');
    } else if (step == 2) {
      this.page_creation_forms['monitors'] = form.value;
      this.activate_page_creation_mode('details');
    } else if (step == 3) {
      if (form.valid) {
        this.creation_in_progress = true;
        let form_data = this.build_form_data(form);
        this.server.create_user_page(form_data).subscribe((res) => {
          if (res.status && res.status == 200) {
            this.refresh_user_pages();
            this.show_creation_window();
            this.shared.show_alert('Page created successfully');
            form.reset();
            this.monitors.forEach((monitor) => (monitor.selected = false));
            this.page_creation_active_index = 0;
            this.activate_page_creation_mode('page');
          }
          this.creation_in_progress = false;
        });
      } else {
        for (let i in form.value) {
          if (form.value[i].length == 0) {
            this.monitor_form_validation[i] = true;
          }
        }
      }
    }
  }

  change_active_page(step: number) {
    if (step == 0) {
      if (
        this.page_creation_active_index ==
        this.pages_marketplace.length - 1
      ) {
        this.page_creation_active_index = 0;
      } else {
        this.page_creation_active_index += 1;
      }
    } else {
      if (this.page_creation_active_index == 0) {
        this.page_creation_active_index = this.pages_marketplace.length - 1;
      } else {
        this.page_creation_active_index -= 1;
      }
    }
  }

  load_icon_file(event: any) {
    this.icon_file = event.target.files[0];
  }

  select_monitor(index: number) {
    this.monitors[index].selected = !this.monitors[index].selected;
  }

  activate_page_creation_mode(mode: string) {
    for (let i in this.page_creations_modes) {
      this.page_creations_modes[i] = false;
    }
    this.page_creations_modes[mode] = true;
  }

  build_form_data(form: NgForm) {
    let form_data = new FormData();
    form_data.append(
      'page_id',
      this.pages_marketplace[this.page_creation_active_index].id
    );
    form_data.append(
      'monitors',
      String(
        this.monitors
          .filter((monitor) => monitor.selected)
          .map((monitor) => monitor.id)
      )
    );
    for (let i in form.value) {
      form_data.append(i, form.value[i]);
    }
    if (this.icon_file) {
      form_data.append('image', this.icon_file, this.icon_file.name);
    }
    return form_data;
  }

  refresh_user_pages() {
    this.loading_pages = true;
    this.server.get_user_pages().subscribe((res) => {
      if (res.status && res.status == 200) {
        this.pages = res.pages;
        this.loading_pages = false;
      }
    });
  }
}
