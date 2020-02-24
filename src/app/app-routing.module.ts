import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OverviewComponent } from "./overview/overview.component";
import { ProjectComponent } from "./project/project.component";
import { ProjectFormComponent } from "./project-form/project-form.component";
import { BrowserComponent } from "./project/browser/browser.component";

const routes: Routes = [
  {
    path: '',
    component: OverviewComponent,
  }, {
    path: 'add-project',
    component: ProjectFormComponent,
  }, {
    path: 'project/:project_id',
    children: [
      {path: 'info', component: ProjectComponent},
      {path: 'browse', component: BrowserComponent},
      {path: 'browse/:path', component: BrowserComponent},
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
