import { Pipe, PipeTransform } from '@angular/core';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';
import { DispensableResult } from '../model/dispensable-result';

@Pipe({
  name: 'markClasses'
})
export class MarkClassesPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) { }

  transform(value: string, result: DispensableResult, finalAspectDict: any): SafeHtml {

    value = this.replaceByMarking('winner', [result.winner], value);
    value = this.replaceByMarking('looser', [result.looser], value);
    value = this.replaceByMarking('aspect', Object.keys(finalAspectDict), value);
    value = this.replaceByMarking('link', result.looserLinks, value);
    value = this.replaceByMarking('link', result.winnerLinks, value);

    return this.sanitizer.bypassSecurityTrustHtml(value);
  }

  private replaceByMarking(type: string, toMark: Array<string>, value: string) {
    for (const mark of toMark) {
      value = value.replace(this.buildRegex(mark), match => {
        return `<span class="${type}">${match}</span>`;
      });
    }
    return value;
  }

  private buildRegex(sequence: string) {
    const regex1 = '(?!<span[^>]*?>)(\\b';
    const regex2 = '\\b)(?![^<]*?</span>)';
    const cleanedsequence = sequence.replace(/[^a-zA-Z0-9 ]/g, ' ').replace(/ +/g, ' ');
    return new RegExp(`${regex1}${sequence}${regex2}|${regex1}${cleanedsequence}${regex2}`, 'gi');
  }

}
