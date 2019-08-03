import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OverviewComponent } from "./overview/overview.component";
import { ProjectComponent } from "./project/project.component";
import { ProjectFormComponent } from "./project-form/project-form.component";

const routes: Routes = [
  {
    path: '',
    component: OverviewComponent,
  }, {
    path: 'add-project',
    component: ProjectFormComponent,
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
