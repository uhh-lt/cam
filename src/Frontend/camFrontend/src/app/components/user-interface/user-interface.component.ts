import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { UrlBuilderService } from '../../shared/url-builder.service';
import { HTTPRequestService } from '../../shared/http-request.service';
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

  aspects = new Array<Aspect>(new Aspect('')); // the rows of aspects currently shown in the UI
  private finalAspDict = {}; // holds all aspects after compare() was called
  selectedModel = 'default'; // the comparison model to be used
  fastSearch = false; // the possibility to do a fast comparison
  showLoading = false; // boolean that checks if the loading screen should be shown
  showResult = false; // boolean that checks if the result table should be shown
  status = '';

  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered

  private statusID = '-1';

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

  constructor(private urlBuilderService: UrlBuilderService, private httpRequestService: HTTPRequestService,
    private snackBar: MatSnackBar, private scrollToService: ScrollToService) { }

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
      if (aspect.value !== '' && aspect.value !== undefined) {
        this.finalAspDict[aspect.value] = aspect.weight;
      }
    }
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
          this.resultPresentation.saveResult(data, this.finalAspDict);
          this.showLoading = false; // hide the loading screen
          this.showResult = true;
          this.status = '';

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
  }

  resetInput() {
    this.object_A = '';
    this.object_B = '';
    this.aspects = new Array<Aspect>(new Aspect(''));
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

  /**
   * Adds an aspect to the list of currently shown aspects.
   *
   */
  addAspect() {
    this.aspects.push(new Aspect(''));
  }

  /**
   * Removes an aspect from the list of currently shown aspects which makes the UI remove this
   * aspect row.
   *
   * @param aspect the aspect row to be removed, given as a number
   */
  removeAspect(aspect: number) {
    this.aspects.splice(aspect, 1);
    if (this.aspects.length === 0) {
      this.addAspect();
    }
  }

  chipSelected(selectedChip: string) {
    if (this.aspects[this.aspects.length - 1].value === '') {
      this.aspects[this.aspects.length - 1].value = selectedChip;
    } else {
      this.aspects.push(new Aspect(selectedChip));
    }
  }
}
