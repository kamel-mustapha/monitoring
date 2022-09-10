import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { MainComponent } from './main/main.component';
import { HomeComponent } from './main/home/home.component';
import { StatsComponent } from './main/stats/stats.component';
import { ProfileComponent } from './main/profile/profile.component';
import { SettingsComponent } from './main/settings/settings.component';
import { HeaderComponent } from './main/header/header.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    MainComponent,
    HomeComponent,
    StatsComponent,
    ProfileComponent,
    SettingsComponent,
    HeaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
