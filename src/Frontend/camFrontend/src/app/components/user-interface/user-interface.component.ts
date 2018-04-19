import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { UrlBuilderService } from '../../shared/url-builder.service';
import { HTTPRequestService } from '../../shared/http-request.service';
import { Result } from '../../model/result';
import { ResultPresentationComponent } from '../result-presentation/result-presentation.component';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-user-interface',
  templateUrl: './user-interface.component.html',
  styleUrls: ['./user-interface.component.css']
})
export class UserInterfaceComponent implements OnInit, AfterViewInit {

  @ViewChild(ResultPresentationComponent) resultPresentation: ResultPresentationComponent;

  aspects = [1]; // the rows of aspects currently shown in the UI
  private aspectDict = {}; // the aspects currently entered
  private finalAspDict = {}; // holds all aspects after compare() was called
  private weightDict = { 1: 1 }; // the weightings of the aspects currently chosen with the sliders
  selectedModel = 'default'; // the comparison model to be used
  fastSearch = false; // the possibility to do a fast comparison
  showLoading = false; // boolean that checks if the loading screen should be shown
  showResult = false; // boolean that checks if the result table should be shown

  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered

  private preSelectedObjects = [
    ['python', 'java'],
    ['php', 'javascript'],
    ['perl', 'python'],
    ['ios', 'android'],
    ['cuda', 'opencl'],
    ['bluetooth', 'ethernet'],
    ['bmw', 'toyota'],
    ['apple', 'microsoft'],
    ['gamecube', 'ps2'],
    ['milk', 'beer'],
    ['motorcycle', 'truck'],
    ['oregon', 'michigan'],
    ['pepsi', 'coca-cola'],
    ['potato', 'steak'],
    ['tennis', 'golf']
  ];

  constructor(private urlbuilderService: UrlBuilderService, private httpRequestService: HTTPRequestService,
    private snackBar: MatSnackBar) { }

  ngOnInit() {
    const index = Math.floor(Math.random() * 15);
    this.object_A = this.preSelectedObjects[index][0];
    this.object_B = this.preSelectedObjects[index][1];
  }

  ngAfterViewInit() {
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
      error => {
        this.snackBar.open('The API-Service seems to be unavailable at the moment :/', '', {
          duration: 3500,
        });
        this.showLoading = false;
        console.error(error);

      },
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
    this.aspectDict = {};
    this.weightDict = { 1: 1 };
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
