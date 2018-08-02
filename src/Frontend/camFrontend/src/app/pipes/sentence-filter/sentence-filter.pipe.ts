import { Pipe, PipeTransform } from '@angular/core';
import { Sentence } from '../../model/sentence';

@Pipe({
  name: 'sentenceFilter'
})
export class SentenceFilterPipe implements PipeTransform {

  transform(sentences: Array<Sentence>, selectedAspects: Array<string>, selectEnteredAspects: Array<string>, trigger: number): any {
    return sentences.filter(sentence =>
      this.allAspectsContained(sentence.text, selectedAspects.concat(selectEnteredAspects))
    );
  }

  allAspectsContained(sentence: string, selectedAspects: Array<string>) {
    if (selectedAspects.length === 0) {
      return true;
    }
    for (const aspect of selectedAspects) {
      if (sentence.toLowerCase().includes(aspect.toLowerCase())) {
        return true;
      }
    }
    return false;
  }

}
