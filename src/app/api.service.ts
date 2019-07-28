import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(
    protected http: HttpClient
  ) { }

  public async get_projects(): Promise<any[]> {
    return new Promise((resolve, reject) => {
      this.http.get('/api/project')
        .subscribe((value: any) => {
          return resolve(value.data as any[]);
        }, (error) => {
          return reject(error);
        });
    });
  }

  public async get_project(id: number): Promise<any> {
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
}
