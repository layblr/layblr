import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import {StepService} from "../../step.service";
import {ExportService} from "../../export.service";

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.scss']
})
export class ExportComponent implements OnInit {

  private exporting: boolean = false;
  private exportResult: any = null;

  constructor(
    private router: Router,
    private stepService: StepService,
    private exportService: ExportService,
  ) { }

  get numFrames() {
    return Object.keys(this.stepService.frames).length
  }

  ngOnInit() {
    if (!this.stepService.audioFile || !this.stepService.featuresFile) {
      this.router.navigateByUrl('/input');
      return;
    }
    if (!this.stepService.sampleRate || !this.stepService.totalDuration || !this.stepService.totalSplits || !this.stepService.splitDuration) {
      this.router.navigateByUrl('/options');
      return;
    }
    if (!this.stepService.frames) {
      this.router.navigateByUrl('/player');
      return;
    }
  }

  exportFilename(type: string) {
    if (type === 'classified_features') {
      return this.stepService.featuresFile.replace('.csv', '_classified.csv');
    } else if (type === 'separate_classes_per_split') {
      return this.stepService.featuresFile.replace('.csv', '_classes_per_split.csv');
    } else if (type === 'separate_classes_per_frame') {
      return this.stepService.featuresFile.replace('.csv', '_classes_per_frame.csv');
    }
    return '?';
  }

  async executeExport(type: string) {
    if (this.exporting) {
      alert('Already exporting!');
      return;
    }
    this.exporting = true;

    // Execute the backend API call to export to the wanted file and with the given info.
    try {
      console.log(this.stepService.frames);
      this.exportResult = await this.exportService.createExport({
        audioFile: this.stepService.audioFile,
        featuresFile: this.stepService.featuresFile,
        exportType: type,
        exportFile: this.exportFilename(type),
        sampleRate: this.stepService.sampleRate,
        totalDuration: this.stepService.totalDuration,
        totalSplits: this.stepService.totalSplits,
        splitDuration: this.stepService.splitDuration,
        classifyCategories: this.stepService.classifyCategories,
        frames: this.stepService.frames,
      });
    } catch (err) {
      alert('Some error happened!');
      console.error(err);
    } finally {
      this.exporting = false;
    }
  }
}
