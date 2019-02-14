import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { UrlBuilderService } from '../../services/url-builder.service';
import { HTTPRequestService } from '../../services/http-request.service';
import { ResultPresentationComponent } from '../result-presentation/result-presentation.component';
import { MatSnackBar } from '@angular/material';
import { TimerObservable } from 'rxjs/observable/TimerObservable';
import { ScrollToService, ScrollToConfigOptions } from '@nicky-lenaers/ngx-scroll-to';
import 'rxjs/add/operator/takeWhile';
import { Aspect } from '../../model/aspect';

@Component({
  selector: 'app-user-interface',
  templateUrl: './user-interface.component.html',
  styleUrls: ['./user-interface.component.css']
})
export class UserInterfaceComponent implements OnInit, AfterViewInit {

  @ViewChild(ResultPresentationComponent) resultPresentation: ResultPresentationComponent;

  private finalAspDict = {}; // holds all aspects after compare() was called
  selectedModel = 'default'; // the comparison model to be used
  fastSearch = false; // the possibility to do a fast comparison
  showLoading = false; // boolean that checks if the loading screen should be shown
  showResult = false; // boolean that checks if the result table should be shown
  showStartText = false;
  showNextText = false;
  showSkipText = false;
  showLastText = false;
  showSkipLastText = false;
  showExportedText = false;
  showExportingText = false;
  showCreatingSentenceExamplesText = false;
  showCreatedSentenceExamplesText = false;
  status = '';

  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered

  private objectA: string;
  private objectB: string;
  private aspectsA: Array<string>;
  private aspectsB: Array<string>;
  private sentencesA: Array<string>;
  private sentencesB: Array<string>;

  private statusID = '-1';

  private generatedAspects = [];

  private preSelectedObjects = [];
  private indexOfSelectedObject = 0;

  constructor(private urlBuilderService: UrlBuilderService, private httpRequestService: HTTPRequestService,
    private snackBar: MatSnackBar, private scrollToService: ScrollToService) { }

  ngOnInit() {
    this.httpRequestService.getPredefinedPairs(this.urlBuilderService.getPredefinedPairsURL()).subscribe(data => {
      this.preSelectedObjects = data;
    });
    this.showStartText = true;
  }

  ngAfterViewInit() {
  }

  /**
   * Reads the input from the UI, starts the search request and calls the save method.
   */
  compare() {
    this.showLoading = true; // show the loading screen
    this.reset(); // reset everything to its default and hide the result table
    // read the objects entered, build the URL and start the search request
    this.httpRequestService.register(this.urlBuilderService.getRegisterURL()).subscribe(
      data => {
        this.statusID = data;
        this.requestScores();
        this.getStatus();
      },
      error => { console.error(error); }
    );
  }

  requestScores() {
    this.httpRequestService.getScore(this.urlBuilderService.buildURL(this.object_A, this.object_B, this.finalAspDict,
      this.selectedModel, this.fastSearch, this.statusID)).subscribe(
        data => {
          this.resultPresentation.saveResult(data);
          this.generatedAspects = data.extractedAspectsObject1.concat(data.extractedAspectsObject2);
          this.showLoading = false; // hide the loading screen
          this.showResult = true;
          this.status = '';

          this.objectA = data.object1.name;
          this.objectB = data.object2.name;
          this.aspectsA = data.extractedAspectsObject1;
          this.aspectsB = data.extractedAspectsObject2;

          this.sentencesA = [];
          this.sentencesB = [];

          for (const sentence of data.object1.sentences) {
            this.sentencesA.push(sentence.text);
          }
          for (const sentence of data.object2.sentences) {
            this.sentencesB.push(sentence.text);
          }

          const config: ScrollToConfigOptions = {
            target: 'resultPresentation'
          };
          this.scrollToService.scrollTo(config);

          this.httpRequestService.removeStatus(this.urlBuilderService.getRemoveStatusURL(this.statusID));
          this.statusID = '-1';
        },
        error => {
          this.snackBar.open('The API-Service seems to be unavailable at the moment :/', '', {
            duration: 3500,
          });
          this.showLoading = false;
          console.error(error);
        }
      );
  }

  submitRatingsToBackend(markedAspects: Array<string>) {
    const aspectDictA = {}
    for (let index = 0; index < this.aspectsA.length; index++) {
      const element = this.aspectsA[index];
      if (markedAspects.indexOf(element) > -1) {
        aspectDictA[element] = 1;
      } else {
        aspectDictA[element] = 0;
      }
    }

    for (const aspect of Object.keys(aspectDictA)) {
      const sentexs = this.getSentexs(aspect, this.sentencesA);

      this.httpRequestService.register(this.urlBuilderService.buildSqlAspectSavingURLA(this.objectA, this.objectB, aspect, aspectDictA[aspect], sentexs)).subscribe(_data => {
      });
    }
    
    const aspectDictB = {}
    for (let index = 0; index < this.aspectsB.length; index++) {
      const element = this.aspectsB[index];
      if (markedAspects.indexOf(element) > -1) {
        aspectDictB[element] = 1;
      } else {
        aspectDictB[element] = 0;
      }
    }

    for (const aspect of Object.keys(aspectDictB)) {
      const sentexs = this.getSentexs(aspect, this.sentencesB);

      this.httpRequestService.register(this.urlBuilderService.buildSqlAspectSavingURLB(this.objectA, this.objectB, aspect, aspectDictB[aspect], sentexs)).subscribe(_data => {
      });
    }
    this.prepareNextComparison(false);
  }

  getSentexs(aspect: string, sentenceList: Array<string>) {
    const sentexs = new Array<string>();
    const re1 = /;/gi;
    const re2 = /&/gi;
    const re3 = /\"/gi;

    for (const sentence of sentenceList) {
      if (sentence.indexOf(aspect) > -1) {
        sentexs.push(sentence.replace(re1, ",").replace(re2, " and ").replace(re3, ""));
        if (sentexs.length > 4) {
          break;
        }
      }
    }

    while (sentexs.length < 5) {
      sentexs.push("");
    }

    return sentexs;
  }

  exportRatings() {
    this.resetTextsShown();
    this.showExportingText = true;
    this.httpRequestService.register(this.urlBuilderService.buildExportRatingsURL()).subscribe(_data => {
      this.resetTextsShown();
      this.showExportedText = true;
    });
  }

  createSentenceExamples() {
    this.resetTextsShown();
    this.showCreatingSentenceExamplesText = true;
    this.httpRequestService.register(this.urlBuilderService.buildCreateSentenceExamplesURL()).subscribe(_data => {
      this.resetTextsShown();
      this.showCreatedSentenceExamplesText = true;
    });
  }

  skipPair() {
    this.prepareNextComparison(true);
  }

  prepareNextComparison(skipped) {
    this.reset();
    this.showLoading = false;
    if (this.indexOfSelectedObject + 1 < this.preSelectedObjects.length) {
      this.indexOfSelectedObject++;
      if (skipped) {
        this.showSkipText = true;
      } else {
        this.showNextText = true;
      }
    } else {
      this.indexOfSelectedObject = 0;
      if (skipped) {
        this.showSkipLastText = true;
      } else {
        this.showLastText = true;
      }
    }
    this.object_A = this.preSelectedObjects[this.indexOfSelectedObject][0];
    this.object_B = this.preSelectedObjects[this.indexOfSelectedObject][1];
  }

  start() {
    this.object_A = this.preSelectedObjects[this.indexOfSelectedObject][0];
    this.object_B = this.preSelectedObjects[this.indexOfSelectedObject][1];
    this.showStartText = false;
  }

  getStatus() {
    TimerObservable.create(0, 500).takeWhile(() => this.showLoading).subscribe(() => {
      this.httpRequestService.getStatus(this.urlBuilderService.getStatusURL(this.selectedModel, this.statusID)).subscribe(
        data => {
          this.status = data;
        },
        error => { console.error(error); }
      );
    });
  }

  /**
   * reset all results to its default and hide the result table.
   *
   */
  reset() {
    this.showResult = false;
    this.finalAspDict = {};
    this.resultPresentation.reset();
    this.resetTextsShown();
  }


  resetTextsShown() {
    this.showStartText = false;
    this.showNextText = false;
    this.showLastText = false;
    this.showSkipText = false;
    this.showSkipLastText = false;
    this.showExportedText = false;
    this.showExportingText = false;
    this.showCreatingSentenceExamplesText = false;
    this.showCreatedSentenceExamplesText = false;
  }

  resetInput() {
    this.object_A = '';
    this.object_B = '';
    this.fastSearch = false;
    this.selectedModel = 'default';
  }

  /**
   * Checks if the user entered something in both the first and the second object fields.
   *
   * @returns true, if the user entered something in both fields, false if not
   */
  objectsEntered() {
    return this.object_A !== '' && this.object_B !== '';
  }

  /**
   * Calls compare() if the user entered something in both the first and the second object fields.
   *
   */
  compIfEntered() {
    if (this.objectsEntered()) {
      this.compare();
    }
  }
}
