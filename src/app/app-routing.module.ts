import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OverviewComponent } from "./overview/overview.component";
import {ProjectComponent} from "./project/project.component";

const routes: Routes = [
  {
    path: '',
    component: OverviewComponent,
  }, {
    path: 'project/:project_id',
    component: ProjectComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
