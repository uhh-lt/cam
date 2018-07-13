import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'sentenceFilter'
})
export class SentenceFilterPipe implements PipeTransform {

  transform(sentences: Array<string>, selectedAspects: Array<string>, trigger: number): any {
    return sentences.filter(sentence =>
      this.allAspectsContained(sentence, selectedAspects)
    );
  }

  allAspectsContained(sentence: string, selectedAspects: Array<string>) {
    for (const aspect of selectedAspects) {
      if (!sentence.includes(aspect)) {
        return false;
      }
    }
    return true;
  }

}
