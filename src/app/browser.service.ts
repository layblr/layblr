import { Injectable } from '@angular/core';
import {FileEntry} from "./browse-modal/browse-modal.component";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class BrowserService {
  constructor(
    private http: HttpClient
  ) { }

  async fetchList(type: string): Promise<FileEntry[]> {
    let url = '/ajax/browse';
    return new Promise<FileEntry[]>((resolve, reject) => {
      this.http.get(url, {
        params: {
          type: type
        }
      }).subscribe((data: any) => {
        resolve(data.files);
      });
    });
  }
}
