import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { FormsModule } from "@angular/forms";
import { HttpClientModule } from "@angular/common/http";
import { ProjectComponent } from './project/project.component';
import { OverviewComponent } from './overview/overview.component';
import { ProjectFormComponent } from './project-form/project-form.component';
import { BrowserComponent } from './project/browser/browser.component';
import { HumanSizePipe } from './human-size.pipe';

@NgModule({
  declarations: [
    AppComponent,
    ProjectComponent,
    OverviewComponent,
    ProjectFormComponent,
    BrowserComponent,
    HumanSizePipe,
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
