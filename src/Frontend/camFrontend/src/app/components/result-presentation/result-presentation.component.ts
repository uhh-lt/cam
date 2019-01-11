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
  @Output() submitAspectsA = new EventEmitter<Array<string>>();
  @Output() submitAspectsB = new EventEmitter<Array<string>>();
  @Output() submitRatingsA = new EventEmitter<Array<string>>();
  @Output() submitRatingsB = new EventEmitter<Array<string>>();
  @Output() submitSentexsA = new EventEmitter<Array<Array<string>>>();
  @Output() submitSentexsB = new EventEmitter<Array<Array<string>>>();
  @Output() skipRating = new EventEmitter();

  private dispensableResult = new DispensableResult();
  private categoriesChartOrder = new Array<string>();
  private none = 'none';          // label for sentences with no contained aspect
  private multiple = 'multiple';  // label for sentences with multiple aspects
  private categoryLabels = {};

  public selectedWinnerAspects = new Array<string>();
  public selectedLooserAspects = new Array<string>();

  private aspectsA: Array<string>;
  private aspectsB: Array<string>;
  private ratingsA = new Array();
  private ratingsB = new Array();
  private sentexsA = new Array();
  private sentexsB = new Array();

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
    this.aspectsA = result.extractedAspectsObject1;
    this.aspectsB = result.extractedAspectsObject2;

    for (const aspect of this.aspectsA) {
      this.ratingsA.push('0');
    }
    
    for (const aspect of this.aspectsB) {
      this.ratingsB.push('0');
    }

    for (const aspect of this.aspectsA) {
      let index = 1;
      for (const sentence of result.object1.sentences) {
        if (sentence.text.indexOf(aspect) > -1) {
          if (index === 1) {
            this.sentexsA[this.aspectsA.indexOf(aspect)] = new Array();
          }
          this.sentexsA[this.aspectsA.indexOf(aspect)].push(sentence.text);
          index++;
          if (index > 3) {
            break;
          }
        };
      }
    }

    for (const aspect of this.aspectsB) {
      let index = 1;
      for (const sentence of result.object2.sentences) {
        if (sentence.text.indexOf(aspect) > -1) {
          if (index === 1) {
            this.sentexsB[this.aspectsB.indexOf(aspect)] = new Array();
          }
          this.sentexsB[this.aspectsB.indexOf(aspect)].push(sentence.text);
          index++;
          if (index > 3) {
            break;
          }
        };
      }
    }

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
      for (const aspect of this.aspectsA) {
        if (markedAspects.indexOf(aspect) > -1) {
          this.ratingsA[this.aspectsA.indexOf(aspect)] = 1;
        } else {
          this.ratingsA[this.aspectsA.indexOf(aspect)] = 0;
        }
      }
    } else {
      for (const aspect of this.aspectsB) {
        if (markedAspects.indexOf(aspect) > -1) {
          this.ratingsB[this.aspectsB.indexOf(aspect)] = 1;
        } else {
          this.ratingsB[this.aspectsB.indexOf(aspect)] = 0;
        }
      }
    }
  }


  openLink(url: string) {
    window.open(url, '_blank');
  }

  submitAspectRatings() {
    this.submitAspectsA.emit(this.aspectsA);
    this.submitAspectsB.emit(this.aspectsB);
    this.submitSentexsA.emit(this.sentexsA);
    this.submitSentexsB.emit(this.sentexsB);
    this.submitRatingsA.emit(this.ratingsA);
    this.submitRatingsB.emit(this.ratingsB);
  }

  skip() {
    this.skipRating.emit();
  }
}
