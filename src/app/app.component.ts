import {Component, OnInit} from '@angular/core';
import {Location} from '@angular/common';
import {Router} from "@angular/router";

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
