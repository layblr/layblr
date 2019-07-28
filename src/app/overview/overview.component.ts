import { Component, OnInit } from '@angular/core';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})
export class OverviewComponent implements OnInit {
  protected projects: any[] = [];

  constructor(
    protected api: ApiService
  ) { }

  async ngOnInit() {
    this.projects = await this.api.get_projects();
  }

}
