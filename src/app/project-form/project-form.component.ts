import { Component, OnInit } from '@angular/core';
import {Project} from "../model/project";
import {ApiService} from "../api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.scss']
})
export class ProjectFormComponent implements OnInit {
  public customLocation: boolean = false;
  public project: Project;

  constructor(
    protected api: ApiService,
    protected router: Router,
  ) { }

  ngOnInit() {
    this.project = new Project();
  }

  async submit() {
    if (! this.project.id && ! this.customLocation) {
      this.project.location = null;
    }
    let project = await this.api.createProject(this.project);
    this.project.id = project.id;
    this.project.location = project.location;

    await this.router.navigateByUrl('/');
  }
}
