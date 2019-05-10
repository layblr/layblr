import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { BrowseModalComponent } from "../../browse-modal/browse-modal.component";
import { Router } from "@angular/router";
import { StepService } from "../../step.service";
import { ImportService } from "../../import.service";

@Component({
  selector: 'app-import',
  templateUrl: './import.component.html',
  styleUrls: ['./import.component.scss']
})
export class ImportComponent implements OnInit {
  @ViewChild(BrowseModalComponent) browseModal: BrowseModalComponent;

  public loading: boolean = false;

  constructor(
    private router: Router,
    private importService: ImportService,
    private stepService: StepService,
  ) { }

  ngOnInit() {

  }

  async browse(type: string) {
    let result = await this.browseModal.browse(type);
    if (type === 'audio') {
      this.stepService.audioFile = result.name;
    } else if (type === 'predictions') {
      this.stepService.predictionsFile = result.name;
    }
  }

  async load() {
    await this.stepService.save();

    this.loading = true;
    let data = await this.importService.loadImport({
      audioFile: this.stepService.audioFile,
      predictionsFile: this.stepService.predictionsFile,
    });
    await this.stepService.loadFromObject({
      audioFile: this.stepService.audioFile,
      featuresFile: this.stepService.predictionsFile,
      predictionsFile: this.stepService.predictionsFile,
      sampleRate: data.sample_rate,
      totalDuration: data.total_duration,
      totalSplits: data.total_splits,
      splitDuration: data.split_duration,
      classifyCategories: data.categories,
      frames: data.frames,
    });
    this.loading = false;
    await this.stepService.save();
    await this.router.navigateByUrl('/player');
  }
}
