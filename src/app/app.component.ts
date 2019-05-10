import {Component, OnInit} from '@angular/core';
import {Location} from '@angular/common';
import {StepService} from "./step.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'stamper';

  constructor (
    private stepService: StepService,
    private router: Router,
    private location: Location,
  ) {}

  async ngOnInit() {
    let hasLoaded = await this.stepService.load();
    if (this.router.isActive('/import', false)) {
      return;
    }
    if (hasLoaded) {
      if (Object.keys(this.stepService.frames).length > 0 && this.stepService.audioFile && this.stepService.featuresFile && this.stepService.totalSplits && this.stepService.totalDuration) {
        await this.router.navigateByUrl('/player');
        return;
      } else if (this.stepService.audioFile && this.stepService.featuresFile && this.stepService.totalSplits && this.stepService.totalDuration) {
        await this.router.navigateByUrl('/player');
        return;
      } else if (this.stepService.audioFile && this.stepService.featuresFile) {
        await this.router.navigateByUrl('/options');
        return;
      } else {
        await this.router.navigateByUrl('/input');
        return;
      }
    }
  }

  back() {
    this.location.back();
  }

  async clear() {
    await this.stepService.clear();
    await this.router.navigateByUrl('/input');
  }
}
