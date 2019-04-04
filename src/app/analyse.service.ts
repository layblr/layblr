import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {FileEntry} from "./browse-modal/browse-modal.component";
import {timeout} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class AnalyseService {

  constructor(
    private http: HttpClient
  ) { }

  async analyse(file: string) {
    let url = '/ajax/analyse/' + file;
    return new Promise<FileEntry[]>((resolve, reject) => {
      this.http.get(url)
        .pipe(timeout(15 * 60 * 1000)) // 15 min.
        .subscribe((data: any) => {
          resolve(data.result);
        });
    });
  }
}
