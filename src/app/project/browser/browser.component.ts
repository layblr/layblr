import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {SidebarService} from "../../sidebar.service";
import {Project} from "../../model/project";
import {DirectoryEntry} from "../../model/directory";

@Component({
  selector: 'app-browser',
  templateUrl: './browser.component.html',
  styleUrls: ['./browser.component.scss']
})
export class BrowserComponent implements OnInit {
  public path: string;
  public project: Project;
  public list: DirectoryEntry[] = [];

  constructor(
    protected api: ApiService,
    protected route: ActivatedRoute,
    protected router: Router,
    protected sidebar: SidebarService,
  ) { }

  async ngOnInit() {
    this.project = await this.api.getProject(
      parseInt(this.route.snapshot.paramMap.get('project_id'))
    );
    await this.sidebar.projectSidebar(this.project);

    this.path = '';
    if (this.route.snapshot.paramMap.has('path')) {
      this.path = this.route.snapshot.paramMap.get('path');
    }

    this.list = await this.api.browseDirectory(this.project.id, this.path);
    console.log(this.list);
  }
}
