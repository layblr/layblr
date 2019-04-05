import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {BrowseModalComponent} from "../../browse-modal/browse-modal.component";
import {Router} from "@angular/router";
import {StepService} from "../../step.service";

@Component({
  selector: 'app-input',
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.scss']
})
export class InputComponent implements OnInit {
  @ViewChild(BrowseModalComponent) browseModal: BrowseModalComponent;

  constructor(
    private router: Router,
    private stepService: StepService,
  ) { }

  ngOnInit() {
    this.stepService.featuresFile = 'record_2019-03-20_14-22-52.mp3.csv';
    this.stepService.audioFile = 'record_2019-03-20_14-22-52.mp3';
  }

  async browse(type: string) {
    let result = await this.browseModal.browse(type);
    if (type === 'audio') {
      this.stepService.audioFile = result.name;
    } else if (type === 'features') {
      this.stepService.featuresFile = result.name;
    }
  }

  async next() {
    await this.stepService.save();
    await this.router.navigateByUrl('/options');
  }

}
