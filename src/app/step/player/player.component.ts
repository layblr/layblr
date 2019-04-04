import {Component, OnInit, ViewChild, ElementRef, AfterViewChecked} from '@angular/core';
import { Router } from "@angular/router";
import {Frame, StepService} from "../../step.service";
import {BehaviorSubject} from "rxjs";

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.scss']
})
export class PlayerComponent implements OnInit, AfterViewChecked {
  @ViewChild('classifyContainer') private classifyContainer: ElementRef;
  @ViewChild('player') playerRef: ElementRef;
  private player: HTMLAudioElement;

  private currentTime: number;
  private currentCategory: string|null = null;

  private currentSplitObserver: BehaviorSubject<number>;
  private currentFrameObserver: BehaviorSubject<Frame|null>;

  private updateInterval: any;

  private speedOptions = [
    0.5,
    0.8,
    1.0,
    1.2,
    1.5,
    1.8,
    2.0,
    2.5,
  ];

  constructor(
    private router: Router,
    private stepService: StepService,
  ) {
    this.currentSplitObserver = new BehaviorSubject<number>(this.currentSplit);
    this.currentFrameObserver = new BehaviorSubject<Frame|null>(this.currentFrame);
  }

  get currentFrame() {
    if (this.currentFrameObserver) {
      return this.currentFrameObserver.getValue();
    }
    return null;
  }
  set currentFrame(val) {
    this.currentFrameObserver.next(val);
  }
  get currentSplit() {
    if (this.currentSplitObserver) {
      return this.currentSplitObserver.getValue();
    }
    return 0;
  }
  set currentSplit(val) {
    if (this.currentSplitObserver && this.currentSplitObserver.getValue() !== val) {
      this.currentSplitObserver.next(val);
    }
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

    this.player = this.playerRef.nativeElement;
    this.updateInterval = setInterval(() => {this.pollDuration()}, 50);

    // Update current category based on new frame.
    this.currentFrameObserver.subscribe((frame) => {
      if (frame) {
        this.currentCategory = frame.category;
      } else {
        this.currentCategory = null;
      }
    });

    // Update current frame if current split updated!
    this.currentSplitObserver.subscribe((splitNr) => {
      // Check if we have one for the exact split number.
      if (this.stepService.frames.hasOwnProperty(splitNr)) {
        this.currentFrame = this.stepService.frames[splitNr];
      }

      // Get the closest frame.
      for (let i = splitNr; i >= 0; i--) {
        if (this.stepService.frames.hasOwnProperty(i)) {
          this.currentFrame = this.stepService.frames[i];
          break;
        }
      }
    });
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    try {
      this.classifyContainer.nativeElement.scrollTop = this.classifyContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  formatTime(timeInSeconds) {
    function pad(num, size) {
      return ('000' + num).slice(size * -1);
    }
    let time: any = parseFloat(timeInSeconds).toFixed(3);
    let hours = Math.floor(time / 60 / 60);
    let minutes = Math.floor(time / 60) % 60;
    let seconds = Math.floor(time - minutes * 60);
    let milliseconds = time.slice(-3);

    return pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2) + '.' + pad(milliseconds, 3);
  }

  togglePlay() {
    if (this.player.paused) {
      this.player.play();
    } else {
      this.player.pause();
    }
  }

  pollDuration() {
    let time = Math.round(this.player.currentTime * 1000);
    if (time !== this.currentTime) {
      this.currentTime = time;
    }
    this.currentSplit = Math.floor(time / this.stepService.splitDuration);
  }

  changeTime(source: HTMLInputElement|any) {
    this.player.currentTime = parseInt(source.value) / 1000;
  }
  changeVolume(source: HTMLInputElement|any) {
    this.player.volume = parseInt(source.value) / 100;
  }

  async classify(time: number, category: string) {
    let timeMs = time * 1000;
    let split = Math.floor(timeMs / this.stepService.splitDuration);

    this.currentCategory = category;
    this.stepService.frames[split] = {
      split: split, category: category, time: time
    };

    await this.stepService.save();
  }

  removeFrame(frame: Frame) {
    delete this.stepService.frames[frame.split];
  }

  async next() {
    await this.stepService.save();
    await this.router.navigateByUrl('/export');
  }
}
