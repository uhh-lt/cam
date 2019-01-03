import { EventEmitter, Component, Output } from '@angular/core';
import { DispensableResult } from '../../model/dispensable-result';
import { Result } from '../../model/result';
import { Sentence } from '../../model/sentence';

@Component({
  selector: 'app-result-presentation',
  templateUrl: './result-presentation.component.html',
  styleUrls: ['./result-presentation.component.css']
})
export class ResultPresentationComponent {

  @Output() chipSelected = new EventEmitter<string>();
  @Output() submitRatings = new EventEmitter<Map<string, Map<string, Map<string, string>>>>();
  @Output() skipRating = new EventEmitter();

  private dispensableResult = new DispensableResult();
  private categoriesChartOrder = new Array<string>();
  private none = 'none';          // label for sentences with no contained aspect
  private multiple = 'multiple';  // label for sentences with multiple aspects
  private categoryLabels = {};

  private sentenceCount: number; // total amount of sentences used for comparison

  public selectedWinnerAspects = new Array<string>();
  public selectedLooserAspects = new Array<string>();

  private objectA: string;
  private objectB: string;
  private aspectMapA = new Map<string, Map<string, string>>();
  private aspectMapB = new Map<string, Map<string, string>>();
  private sentencesA: Array<Sentence>;
  private sentencesB: Array<Sentence>;

  public trigger = 0;

  showResult: boolean;

  constructor() {
    this.categoryLabels[this.none] = 'General Comparison';
    this.categoryLabels[this.multiple] = 'Multiple Aspects';

  }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result: Result) {
    // count the number of sentences used for comparison
    this.sentenceCount = result.sentenceCount;

    this.objectA = result.object1.name;
    this.objectB = result.object2.name;

    result.extractedAspectsObject1.forEach(aspect => {
      const newMap = new Map<string, string>();
      newMap.set('rating', '0');
      newMap.set('sentex1', '');
      newMap.set('sentex2', '');
      newMap.set('sentex3', '');
      this.aspectMapA.set(aspect, newMap);
    });
    result.extractedAspectsObject2.forEach(aspect => {
      const newMap = new Map<string, string>();
      newMap.set('rating', '0');
      newMap.set('sentex1', '');
      newMap.set('sentex2', '');
      newMap.set('sentex3', '');
      this.aspectMapB.set(aspect, newMap);
    });

    this.sentencesA = result.object1.sentences;
    this.sentencesB = result.object2.sentences;

    this.aspectMapA.forEach((value: Map<string, string>, aspect: string) => {
      let index = 1;
      this.sentencesA.forEach(sentence => {
        if (index < 4 && sentence.text.indexOf(aspect) > -1) {
          const sentexIndex = 'sentex' + index.toString();
          value.set(sentexIndex, sentence.text);
          index++;
        };
      });
    });
    this.aspectMapB.forEach((value: Map<string, string>, aspect: string) => {
      let index = 1;
      this.sentencesB.forEach(sentence => {
        if (index < 4 && sentence.text.indexOf(aspect) > -1) {
          const sentexIndex = 'sentex' + index.toString();
          value.set(sentexIndex, sentence.text);
          index++;
        };
      });
    });

    if (result.winner === result.object1.name) {
      this.saveWinner(result.object1.name, result.object2.name);
      this.saveScores(result.object1.points, result.object2.points, result.object1.totalPoints, result.object2.totalPoints);
      this.saveExtractedAspects(result.extractedAspectsObject1, result.extractedAspectsObject2);
      this.saveSentences(result.object1.sentences, result.object2.sentences);

    } else {
      this.saveWinner(result.object2.name, result.object1.name);
      this.saveScores(result.object2.points, result.object1.points, result.object2.totalPoints, result.object1.totalPoints);
      this.saveExtractedAspects(result.extractedAspectsObject2, result.extractedAspectsObject1);
      this.saveSentences(result.object2.sentences, result.object1.sentences);
    }
    this.showResult = true;
  }

  reset() {
    this.dispensableResult = new DispensableResult();
    this.sentenceCount = 0;
    this.showResult = false;
    this.selectedWinnerAspects = new Array<string>();
    this.selectedLooserAspects = new Array<string>();
    this.categoriesChartOrder = [];
  }

  /**
   * Save the winner and loser of the comparison.
   *
   * @param winner object that won the comparation
   * @param looser object that lost the comparation
   */
  private saveWinner(winner: string, looser: string) {
    this.dispensableResult.winner = winner;
    this.dispensableResult.looser = looser;
  }

  /**
   * Save the percentage of the scores for each object.
   *
   * @param winnerScore the score of the object that won the comparation
   * @param looserScore the score of the object that lost the comparation
   */
  private saveScores(winnerScores: any, looserScores: any, totalScoreA: number, totalScoreB: number) {

    this.dispensableResult.winnerTotalScore = this.calcScore(totalScoreA, totalScoreB);
    this.dispensableResult.looserTotalScore = this.calcScore(totalScoreB, totalScoreA);
    const categories = Array.from(new Set(Object.keys(winnerScores).concat(Object.keys(looserScores))));
    categories.forEach(key => {
      if (key !== this.none && key !== this.multiple) {
        this.setScores(winnerScores[key], looserScores[key], key);
        this.categoryLabels[key] = key;
      }
    });
    if (categories.indexOf(this.multiple) !== -1) {
      this.setScores(winnerScores[this.multiple], looserScores[this.multiple], this.categoryLabels[this.multiple]);
    }
    if (categories.length > 1) {
      this.setScores(winnerScores[this.none], looserScores[this.none], this.categoryLabels[this.none]);
    }
  }

  private setScores(a: number, b: number, label: string): void {
    this.dispensableResult.winnerScoresPercent[label] = this.calcScore(a, b);
    this.dispensableResult.looserScoresPercent[label] = this.calcScore(b, a);
    this.categoriesChartOrder.push(label);
  }

  private calcScore(a: number, b: number): string {
    if (a === undefined) {
      a = 0;
    }
    if (b === undefined) {
      b = 0;
    }

    return (a / (a + b) * 100).toFixed(2);
  }

  /**
   * Save the extracted aspects for each object.
   *
   * @param winnerAspects aspects of the object that won the comparation
   * @param looserAspects aspects of the object that lost the comparation
   */
  private saveExtractedAspects(winnerAspects: Array<string>, looserAspects: Array<string>) {
    this.dispensableResult.winnerLinks = winnerAspects;
    this.dispensableResult.looserLinks = looserAspects;
  }

  /**
   * Save the clustered sentences each object has won.
   *
   * @param winnerSentences sentences of the object that won
   * @param looserSentences sentences of the object that lost
   */
  private saveSentences(winnerSentences: Array<Sentence>, looserSentences: Array<Sentence>) {
    this.dispensableResult.winnerSentences = winnerSentences;
    this.dispensableResult.looserSentences = looserSentences;
  }


  updatedSelection(selectedAspects: Array<string>, isWinner: boolean) {
    console.log('update selection');
    if (isWinner) {
      this.selectedWinnerAspects = selectedAspects;
    } else {
      this.selectedLooserAspects = selectedAspects;
    }
    this.trigger++;
  }


  updatedMarks(markedAspects: Array<string>, obj) {
    if (obj === 0) {
      this.aspectMapA.forEach((value: Map<string, string>, key: string) => {
        if (markedAspects.indexOf(key) > -1) {
          this.aspectMapA.get(key).set('rating', '1');
        } else {
          this.aspectMapA.get(key).set('rating', '0');
        }
      });
    } else {
      this.aspectMapB.forEach((value: Map<string, string>, key: string) => {
        if (markedAspects.indexOf(key) > -1) {
          this.aspectMapB.get(key).set('rating', '1');
        } else {
          this.aspectMapB.get(key).set('rating', '0');
        }
      });
    }
  }


  openLink(url: string) {
    window.open(url, '_blank');
  }

  submitAspectRatings() {
    const aspectMap = new Map<string, Map<string, Map<string, string>>>();
    aspectMap.set(this.objectA, this.aspectMapA);
    aspectMap.set(this.objectB, this.aspectMapB);
    this.submitRatings.emit(aspectMap);
  }

  skip() {
    this.skipRating.emit();
  }
}
