import { Injectable } from '@angular/core';
import seedColor from 'seed-color';
import { LocalStorage } from "@ngx-pwa/local-storage";

export interface StepStorage {
  audioFile: string,
  featuresFile: string,
  predictionsFile: string,
  sampleRate: number,
  totalDuration: number,
  totalSplits: number,
  splitDuration: number,
  classifyCategories: string[],
  frames: {[s: number]: Frame},
}

export interface Frame {
  split: number,
  category: string,
  time?: number,
}

@Injectable({
  providedIn: 'root'
})
export class StepService implements StepStorage {
  public audioFile: string;
  public featuresFile: string;
  public predictionsFile: string;

  public sampleRate: number;
  public totalDuration: number;
  public totalSplits: number;
  public splitDuration: number;
  public classifyCategories: string[] = ['talk', 'advertisement', 'music', 'other'];

  public frames: {[s: number]: Frame} = {};

  set classifyCategoriesValue(value: string) {
    this.classifyCategories = value.split('\n');
  }
  get classifyCategoriesValue() {
    return this.classifyCategories.join('\n');
  }
  get orderedFrames() {
    return Object.keys(this.frames);
  }

  constructor(
    private localStorage: LocalStorage
  ) { }

  public getClassifierColor(category: string) {
    if (! category) {
      return 'FFFFFF';
    }
    return seedColor(category).toHex();
  }

  public static isStorage(object: any): object is StepStorage {
    return 'audioFile' in object && 'featuresFile' in object
      && 'sampleRate' in object && 'totalDuration' in object
      && 'totalSplits' in object && 'splitDuration' in object
      && 'classifyCategories' in object && 'frames' in object;
  }

  public async save() {
    return new Promise((resolve, reject) => {
      let data = {
        audioFile: this.audioFile,
        featuresFile: this.featuresFile,
        predictionsFile: this.predictionsFile,

        sampleRate: this.sampleRate,
        totalDuration: this.totalDuration,
        totalSplits: this.totalSplits,
        splitDuration: this.splitDuration,

        classifyCategories: this.classifyCategories,

        frames: this.frames,
      };
      this.localStorage.setItem('stamper-session', data).subscribe(() => {
        resolve();
      }, (error) => {
        reject(error);
      });
    });
  }

  public async load() {
    return new Promise((resolve, reject) => {
      this.localStorage.getItem('stamper-session')
        .subscribe((data) => {
          if (StepService.isStorage(data)) {
            this.loadFromObject(data);
            return resolve(true);
          }
          return resolve(false);
        }, (error) => {
          reject(error);
        });
    });
  }

  public loadFromObject(data: StepStorage) {
    this.audioFile = data.audioFile;
    this.featuresFile = data.featuresFile;
    this.predictionsFile = data.predictionsFile;
    this.sampleRate = data.sampleRate;
    this.totalDuration = data.totalDuration;
    this.totalSplits = data.totalSplits;
    this.splitDuration = data.splitDuration;
    this.classifyCategories = data.classifyCategories;
    this.frames = data.frames;
  }

  public async clear() {
    this.audioFile = null;
    this.featuresFile = null;
    this.predictionsFile = null;
    this.sampleRate = null;
    this.totalDuration = null;
    this.totalSplits = null;
    this.splitDuration = null;
    this.classifyCategories = ['talk', 'advertisement', 'music', 'other'];
    this.frames = {};
    await this.localStorage.removeItem('stamper-session');
    await this.save();
  }
}
