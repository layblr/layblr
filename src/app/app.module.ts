import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { InputComponent } from './step/input/input.component';
import { OptionsComponent } from './step/options/options.component';
import { PlayerComponent } from './step/player/player.component';
import { FormsModule } from "@angular/forms";
import { BrowseModalComponent } from './browse-modal/browse-modal.component';
import { HttpClientModule } from "@angular/common/http";
import { ExportComponent } from './step/export/export.component';
import { ImportComponent } from "./step/import/import.component";

@NgModule({
  declarations: [
    AppComponent,

    InputComponent,
    OptionsComponent,
    PlayerComponent,
    BrowseModalComponent,
    ExportComponent,
    ImportComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
