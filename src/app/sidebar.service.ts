import { Injectable } from '@angular/core';
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class SidebarService {
  public active: boolean = false;
  public menu: Menu = null;
  public project: any = null;

  constructor(
    private router: Router
  ) { }

  get activeItem(): MenuItem|null {
    return null;
  }

  get items (): MenuItem[] {
    if (this.menu) {
      return this.menu.items;
    }
    return [];
  }

  async projectSidebar(project) {
    this.project = project;

  }
}

export class MenuItem {
  public name: string;
  public submenu: Menu|null = null;

}

export class Menu {
  public name: string = null;
  public items: MenuItem[] = [];
}
