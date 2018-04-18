import { Pipe, PipeTransform } from '@angular/core';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';
import { Result } from '../model/result';

@Pipe({
  name: 'markClasses'
})
export class MarkClassesPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) { }

  transform(value: string, result: Result, finalAspectDict: any): SafeHtml {

    const regex1 = '(?!<span[^>]*?>)(\\b';
    const regex2 = '\\b)(?![^<]*?</span>)';

    value = value.replace(new RegExp(regex1 + result.winner + regex2, 'gi'), match => {
      return '<span class="winner">' + result.winner + '</span>';
    });
    value = value.replace(new RegExp(regex1 + result.looser + regex2, 'gi'), match => {
      return '<span class="looser">' + match + '</span>';
    });
    for (const aspect of Object.keys(finalAspectDict)) {
      value = value.replace(new RegExp(regex1 + aspect + regex2, 'gi'), match => {
        return '<span class="aspect">' + match + '</span>';
      });
    }
    for (const link of result.looserLinks) {
      value = value.replace(new RegExp(regex1 + link + regex2, 'gi'), match => {
        return '<span class="link">' + match + '</span>';
      });
    }
    for (const link of result.winnerLinks) {
      value = value.replace(new RegExp(regex1 + link + regex2, 'gi'), match => {
        return '<span class="link">' + match + '</span>';
      });
    }


    return this.sanitizer.bypassSecurityTrustHtml(value);
  }

}
