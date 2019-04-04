import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Frame} from "./step.service";
import {timeout} from "rxjs/operators";

export interface ExportOptions {
  audioFile: string,
  featuresFile: string,

  sampleRate: number,
  totalDuration: number,
  totalSplits: number,
  splitDuration: number,
  classifyCategories: string[],

  frames: {[s: number]: Frame},

  exportType: string,
  exportFile: string,
}

@Injectable({
  providedIn: 'root'
})
export class ExportService {

  constructor(
    private http: HttpClient,
  ) { }

  public async createExport(options: ExportOptions): Promise<string> {
    return new Promise<string>((resolve, reject) => {
      this.http.post('/ajax/export', options)
        .pipe(timeout(15 * 60 * 1000)) // 15 min.
        .subscribe((data: any) => {
          return resolve(data.filename);
        }, (error) => {
          return reject(error);
        });
    });
  }
}
