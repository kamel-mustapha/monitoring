import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './main/home/home.component';
import { StatsComponent } from './main/stats/stats.component';
import { ProfileComponent } from './main/profile/profile.component';
import { SettingsComponent } from './main/settings/settings.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'statistics', component: StatsComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'settings', component: SettingsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
