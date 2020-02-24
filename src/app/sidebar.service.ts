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
    this.menu = new Menu();
    this.menu.items = [
      new MenuItem('Overview', `project/${this.project.id}/info`),
      new MenuItem('Browse', `project/${this.project.id}/browse`),
    ];
    this.active = true;
  }
}

export class MenuItem {
  public name: string;
  public submenu: Menu|null = null;
  public route: string;
  public params: any;

  public constructor(
    name: string, route: string, params: any = {}
  ) {
    this.name = name;
    this.route = route;
    this.params = params;
  }
}

export class Menu {
  public name: string = null;
  public items: MenuItem[] = [];
}
