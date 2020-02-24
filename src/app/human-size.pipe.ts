import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'human_size',
})
export class HumanSizePipe implements PipeTransform {

  transform(value: any, ...args: any[]): any {
    let kb = value / 1024;
    let mb = kb / 1024;
    let gb = mb / 1024;
    if (gb >= 1) {
      return gb.toFixed(2) + ' GB';
    } else if (mb >- 1) {
      return mb.toFixed(2) + ' MB';
    } else if (kb >= 1) {
      return kb.toFixed(2) + ' KB';
    }
    return value + ' Bytes';
  }

}
