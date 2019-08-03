import { Component, OnInit } from '@angular/core';
import {ApiService} from "../api.service";
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {switchMap} from "rxjs/operators";
import {SidebarService} from "../sidebar.service";

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss']
})
export class ProjectComponent implements OnInit {
  public project: any;

  constructor(
    protected api: ApiService,
    protected sidebar: SidebarService,
    protected route: ActivatedRoute,
    protected router: Router
  ) { }

  async ngOnInit() {
    this.project = await this.api.getProject(
      parseInt(this.route.snapshot.paramMap.get('project_id'))
    );

    await this.sidebar.projectSidebar(this.project);
  }

}
