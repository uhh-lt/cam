import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { UrlBuilderService } from '../../shared/url-builder.service';
import { ClustererService } from '../../shared/clusterer.service';
import { HTTPRequestService } from '../../shared/http-request.service';
import { Result } from '../../model/result';
import { ResultPresentationComponent } from '../result-presentation/result-presentation.component';

@Component({
  selector: 'app-user-interface',
  templateUrl: './user-interface.component.html',
  styleUrls: ['./user-interface.component.css']
})
export class UserInterfaceComponent implements OnInit, AfterViewInit {

  @ViewChild(ResultPresentationComponent) resultPresentation: ResultPresentationComponent;

  private aspects = [1]; // the rows of aspects currently shown in the UI
  private aspectDict = {}; // the aspects currently entered
  private finalAspDict = {}; // holds all aspects after compare() was called
  private weightDict = { 1: 1 }; // the weightings of the aspects currently chosen with the sliders
  private selectedModel = 'default'; // the comparison model to be used
  private fastSearch = false; // the possibility to do a fast comparison
  private showLoading = false; // boolean that checks if the loading screen should be shown
  private showResult = false; // boolean that checks if the result table should be shown

  private object_A = ''; // the first object currently entered
  private object_B = ''; // the second object currently entered

  constructor(private urlbuilderService: UrlBuilderService, private clustererService: ClustererService,
    private httpRequestService: HTTPRequestService) { }

  ngOnInit() {
  }

  ngAfterViewInit() {
    console.log('on after view init', this.resultPresentation);
  }

  /**
   * Reads the input from the UI, starts the search request and calls the save method.
   */
  compare() {
    this.showLoading = true; // show the loading screen
    this.reset(); // reset everything to its default and hide the result table
    // read the aspects entered by the user and store them with their weight
    for (const aspect of this.aspects) {
      if (this.aspectDict[aspect] !== undefined) {
        this.finalAspDict[this.aspectDict[aspect].trim()] = this.weightDict[
          aspect
        ];
      }
    }
    // read the objects entered, build the URL and start the search request
    this.saveObjects();
    const url = this.urlbuilderService.buildURL(this.object_A, this.object_B, this.finalAspDict, this.selectedModel, this.fastSearch);
    this.httpRequestService.getScore(url).subscribe(
      data => { this.resultPresentation.saveResult(data, this.finalAspDict); },       // async res => { await this.saveResult(res);
      error => { console.error(error); },
      () => {
        this.showLoading = false; // hide the loading screen
        this.showResult = true;
      }
    );
  }

  /**
   * reset all results to its default and hide the result table.
   *
   */
  reset() {
    this.showResult = false;
    this.finalAspDict = {};
    this.resultPresentation.reset();
  }

  resetInput() {
    this.object_A = '';
    this.object_B = '';
    for (const aspect of Object.keys(this.aspectDict)) {
      this.aspectDict[aspect] = '';
    }
    this.aspects = [1];
    this.fastSearch = false;
  }

  /**
   * Save the trimmed objects that were entered after compare() was called.
   *
   */
  saveObjects() {
    this.object_A = this.object_A.trim();
    this.object_B = this.object_B.trim();
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

  /**
   * Adds an aspect to the list of currently shown aspects.
   *
   */
  addAspect() {
    this.aspects.push(this.aspects[this.aspects.length - 1] + 1);
    this.weightDict[this.aspects[this.aspects.length - 1]] = 1;
  }

  /**
   * Removes an aspect from the list of currently shown aspects which makes the UI remove this
   * aspect row.
   *
   * @param aspect the aspect row to be removed, given as a number
   */
  removeAspect(aspect) {
    if (this.aspects.length > 1) {
      const index = this.aspects.indexOf(aspect, 0);
      if (index > -1) {
        this.aspects.splice(index, 1);
      }
    } else {
      this.aspectDict[this.aspects[0]] = '';
    }
  }
}
