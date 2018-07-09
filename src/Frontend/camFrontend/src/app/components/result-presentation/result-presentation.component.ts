import { Component } from '@angular/core';
import { DispensableResult } from '../../model/dispensable-result';
import { Result } from '../../model/result';

@Component({
  selector: 'app-result-presentation',
  templateUrl: './result-presentation.component.html',
  styleUrls: ['./result-presentation.component.css']
})
export class ResultPresentationComponent {

  private dispensableResult = new DispensableResult();
  private finalAspectDict = {};

  private sentenceCount: number; // total amount of sentences used for comparison

  public selectedWinnerAspects = new Array<string>();
  public selectedLooserAspects = new Array<string>();
  public trigger = 0;

  showResult: boolean;

  constructor() { }

  /**
   * Saves the search result so that they can be shown in the UI.
   *
   * @param result the search results to be saved
   */
  saveResult(result: Result, finalAspDict) {
    console.log('Save Result accessed');
    this.finalAspectDict = finalAspDict;

    // count the number of sentences used for comparison
    this.sentenceCount = result.sentencesObject1.length + result.sentencesObject2.length;

    const aWon = result.scoreObject1 > result.scoreObject2; // did object A win?
    if (aWon) {
      this.saveWinner(result.object1, result.object2);
      this.saveScores(result.scoreObject1, result.scoreObject2);
      this.saveExtractedAspects(result.extractedAspectsObject1, result.extractedAspectsObject2);
      this.saveSentences(result.sentencesObject1, result.sentencesObject2);

    } else {
      this.saveWinner(result.object2, result.object1);
      this.saveScores(result.scoreObject2, result.scoreObject1);
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
  private saveScores(winnerScore: number, looserScore: number) {
    this.dispensableResult.winnerScorePercent = (winnerScore / (winnerScore + looserScore) * 100).toFixed(2);
    this.dispensableResult.looserScorePercent = (looserScore / (winnerScore + looserScore) * 100).toFixed(2);
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
  private saveSentences(winnerSentences: Array<string>, looserSentences: Array<string>) {
    this.dispensableResult.sentencesObjectA = winnerSentences;
    this.dispensableResult.sentencesObjectB = looserSentences;
  }


  updatedSelection(selectedAspects: Array<string>, isWinner: boolean) {
    if (isWinner) {
      this.selectedWinnerAspects = selectedAspects;
    } else {
      this.selectedLooserAspects = selectedAspects;
    }
    this.trigger++;
  }
}
