import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { InputComponent } from "./step/input/input.component";
import { OptionsComponent } from "./step/options/options.component";
import { PlayerComponent } from "./step/player/player.component";
import { ExportComponent } from "./step/export/export.component";
import {ImportComponent} from "./step/import/import.component";

const routes: Routes = [
  {
    path: 'import',
    component: ImportComponent,
  }, {
    path: 'input',
    component: InputComponent,
  }, {
    path: 'options',
    component: OptionsComponent
  }, {
    path: 'player',
    component: PlayerComponent,
  }, {
    path: 'export',
    component: ExportComponent,
  }, {
    path: '',
    redirectTo: '/input',
    pathMatch: 'full',
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
