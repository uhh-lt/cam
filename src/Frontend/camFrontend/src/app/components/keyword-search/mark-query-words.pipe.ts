import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'markQueryWords'
})
export class MarkQueryWordsPipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) { }

  transform(sentence: string, keywords: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(this.markKeywords(sentence, keywords));
  }

  private markKeywords(sentence: string, keywords: string) {
    for (const keyword of keywords) {
      sentence = sentence.replace(new RegExp(keyword, 'ig'), `<mark style="background-color: #ffff00;">${keyword}</mark>`);
    }
    return sentence;
  }

}
