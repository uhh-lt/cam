import { EventEmitter, Component, Output } from '@angular/core';
import { DispensableResult } from '../../model/dispensable-result';
import { Result } from '../../model/result';

@Component({
  selector: 'app-result-presentation',
  templateUrl: './result-presentation.component.html',
  styleUrls: ['./result-presentation.component.css']
})
export class ResultPresentationComponent {

  @Output() chipSelected = new EventEmitter<string>();

  private dispensableResult = new DispensableResult();
  private categoriesChartOrder = new Array<string>();
  private none = 'none';          // label for sentences with no contained aspect
  private multiple = 'multiple';  // label for sentences with multiple aspects
  private categoryLabels = {};

  private sentenceCount: number; // total amount of sentences used for comparison

  public selectedWinnerAspects = new Array<string>();
  public selectedLooserAspects = new Array<string>();
  public selectedEnteredAspects = new Array<string>();
  public finalAspectList = new Array<string>();

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
  saveResult(result: Result, finalAspectList: Array<string>) {
    this.finalAspectList = finalAspectList;

    // count the number of sentences used for comparison
    this.sentenceCount = result.sentenceCount;

    if (result.winner === result.object1) {
      this.saveWinner(result.object1, result.object2);
      this.saveScores(result.scoreObject1, result.scoreObject2, result.totalScoreObject1, result.totalScoreObject2);
      this.saveExtractedAspects(result.extractedAspectsObject1, result.extractedAspectsObject2);
      this.saveSentences(result.sentencesObject1, result.sentencesObject2);

    } else {
      this.saveWinner(result.object2, result.object1);
      this.saveScores(result.scoreObject2, result.scoreObject1, result.totalScoreObject2, result.totalScoreObject1);
      this.saveExtractedAspects(result.extractedAspectsObject2, result.extractedAspectsObject1);
      this.saveSentences(result.sentencesObject2, result.sentencesObject1);
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

    this.dispensableResult.looserTotalScore = this.calcScore(totalScoreA, totalScoreB);
    this.dispensableResult.winnerTotalScore = this.calcScore(totalScoreB, totalScoreA);
    const categories = Array.from(new Set(Object.keys(winnerScores).concat(Object.keys(looserScores))));
    this.setScores(winnerScores[this.none], looserScores[this.none], this.categoryLabels[this.none]);
    if (categories.length > 1) {
      categories.forEach(key => {
        if (key !== this.none && key !== this.multiple) {
          this.setScores(winnerScores[key], looserScores[key], key);
          this.categoryLabels[key] = key;
        }
      });

      if (categories.indexOf(this.multiple) !== -1) {
        this.setScores(winnerScores[this.multiple], looserScores[this.multiple], this.categoryLabels[this.multiple]);
      }
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
  private saveSentences(winnerSentences: Array<String>, looserSentences: Array<String>) {
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

  selectEnteredAspects(selectedAspects: Array<string>) {
    console.log('select entered aspects');
    this.selectedEnteredAspects = selectedAspects;
    this.trigger++;
  }

  chiplistSelect(selectedChip: string) {
    this.chipSelected.emit(selectedChip);
  }
}
