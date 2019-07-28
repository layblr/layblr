import { Component, OnInit } from '@angular/core';
import {ApiService} from "../api.service";
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {switchMap} from "rxjs/operators";

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss']
})
export class ProjectComponent implements OnInit {
  protected project: any;

  constructor(
    protected api: ApiService,
    protected route: ActivatedRoute,
    protected router: Router
  ) { }

  async ngOnInit() {
    this.project = await this.api.get_project(
      parseInt(this.route.snapshot.paramMap.get('project_id'))
    );
  }

}
