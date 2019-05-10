import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Frame, StepStorage } from "./step.service";
import { timeout } from "rxjs/operators";

export interface ImportOptions {
  audioFile: string,
  predictionsFile: string,
}

@Injectable({
  providedIn: 'root'
})
export class ImportService {

  constructor(
    private http: HttpClient,
  ) { }

  public async loadImport(options: ImportOptions): Promise<any> {
    return new Promise<any>((resolve, reject) => {
      this.http.post('/ajax/import', options)
        .pipe(timeout(15 * 60 * 1000)) // 15 min.
        .subscribe((data: any) => {
          return resolve(data);
        }, (error) => {
          return reject(error);
        });
    });
  }
}
