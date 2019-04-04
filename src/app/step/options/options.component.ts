import { Component, OnInit } from '@angular/core';
import { StepService } from "../../step.service";
import { Router } from "@angular/router";
import {AnalyseService} from "../../analyse.service";

@Component({
  selector: 'app-options',
  templateUrl: './options.component.html',
  styleUrls: ['./options.component.scss']
})
export class OptionsComponent implements OnInit {
  private loading: boolean = false;

  constructor(
    private router: Router,
    private stepService: StepService,
    private analyseService: AnalyseService,
  ) { }

  ngOnInit() {
    if (!this.stepService.audioFile || !this.stepService.featuresFile) {
      this.router.navigateByUrl('/input');
      return;
    }
  }

  private async analyseAudio(file: string) {
    let result: any = await this.analyseService.analyse(file);
    this.stepService.sampleRate = result.sample_rate;
    this.stepService.totalDuration = Math.round(result.duration * 1000);
  }

  private async analyseFeatures(file: string) {
    let result: any = await this.analyseService.analyse(file);
    this.stepService.totalSplits = result.lines;
  }

  async autoDetect() {
    // Auto Detection consists of two parts, one for the features and one for the audio.
    this.loading = true;

    await Promise.all([
      this.analyseAudio(this.stepService.audioFile),
      this.analyseFeatures(this.stepService.featuresFile)
    ]);

    // Calculate split size.
    this.stepService.splitDuration = this.stepService.totalDuration / this.stepService.totalSplits;

    this.loading = false;
  }

  async next() {
    await this.stepService.save();
    await this.router.navigateByUrl('/player');
  }
}
