import {Component, OnInit} from '@angular/core';
import {Location} from '@angular/common';
import {Router} from "@angular/router";
import {SidebarService} from "./sidebar.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'layblr';

  constructor (
    private router: Router,
    private location: Location,
    public sidebar: SidebarService,
  ) {}

  async ngOnInit() {
    return;
  }

  back() {
    this.location.back();
  }

  async clear() {
    return;
  }
}
