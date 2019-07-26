import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ProjectsComponent} from "./projects/projects.component";

const routes: Routes = [
  {
    path: 'projects',
    component: ProjectsComponent,
  }, {
    path: '',
    redirectTo: '/projects',
    pathMatch: 'full',
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
