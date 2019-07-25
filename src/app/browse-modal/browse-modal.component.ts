import * as $ from "jquery";
import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {BrowserService} from "../browser.service";

export interface FileEntry {
  name: string,
  extension: string,
  size: number,
  human_size: string,
}

@Component({
  selector: 'app-browse-modal',
  templateUrl: './browse-modal.component.html',
  styleUrls: ['./browse-modal.component.scss']
})
export class BrowseModalComponent implements OnInit {
  public isLoading = false;
  public files: FileEntry[] = [];
  public selectedFile: FileEntry|null = null;

  private resolve: any;

  @ViewChild('modal', { static: true }) modal: ElementRef;
  private modalEl: JQuery<HTMLElement> = null;

  constructor(
    private browserService: BrowserService
  ) { }

  ngOnInit() {
    this.modalEl = $(this.modal.nativeElement);
    this.modalEl.modal({show: false});
  }

  async browse(type: string) {
    this.files = [];
    this.selectedFile = null;

    this.display();
    this.files = await this.browserService.fetchList(type);
    this.isLoading = false;

    return new Promise<FileEntry>((resolve, reject) => {
      this.resolve = resolve;
    });
  }

  selectFile(file: FileEntry) {
    this.selectedFile = file;
  }

  display() {
    this.modalEl.modal('show');
    this.isLoading = true;
  }

  done() {
    if (! this.selectedFile) return;
    this.resolve(this.selectedFile);
    this.close();
  }

  close() {
    this.modalEl.modal('hide');
  }
}
