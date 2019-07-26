import { Injectable } from '@angular/core';
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class SidebarService {
  public active: boolean = false;
  public items: {[s:string]: any};

  constructor(
    private router: Router
  ) { }

  get activeItem () {
    return null;
  }
}
