import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Project} from "./model/project";
import {DirectoryEntry} from "./model/directory";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(
    protected http: HttpClient
  ) { }

  public async getProjects(): Promise<any[]> {
    return new Promise((resolve, reject) => {
      this.http.get('/api/project')
        .subscribe((value: any) => {
          return resolve(value.data as any[]);
        }, (error) => {
          return reject(error);
        });
    });
  }

  public async getProject(id: number): Promise<any> {
    return new Promise((resolve, reject) => {
      this.http.get(`/api/project/${id}`)
        .subscribe((value: any) => {
          console.log(value);
          return resolve(value.data);
        }, (error) => {
          return reject(error);
        })
    });
  }

  public async createProject(project: Project): Promise<Project> {
    return new Promise((resolve, reject) => {
      this.http.post('/api/project', {
        name: project.name,
        location: project.location,
      }).subscribe((value: any) => {
        console.log(value);
        return resolve(value.data as Project);
      }, (error: any) => {
        console.error(error);
      });
    });
  }

  public async browseDirectory(projectId: number, subdir: string = ''): Promise<DirectoryEntry[]> {
    return new Promise((resolve, reject) => {
      this.http.get(`/api/project/${projectId}/browse/${subdir}`)
        .subscribe((data: any) => {
          return resolve(data.data.listing as DirectoryEntry[]);
        }, (error) => {
          return reject(error);
        });
    });
  }
}
