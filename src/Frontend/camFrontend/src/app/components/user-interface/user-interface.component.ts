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
  status = '';

  object_A = ''; // the first object currently entered
  object_B = ''; // the second object currently entered

  private statusID = '-1';

  private generatedAspects = [];

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
    const aspectList = {}
    for (let index = 0; index < markedAspects.length; index++) {
      const element = markedAspects[index];
      if (markedAspects.indexOf(element) > -1) {
        aspectList[element] = 1;
      } else {
        aspectList[element] = 0;
      }
    }
    const url = this.urlBuilderService.buildSqliteAspectSavingURL(this.object_A, this.object_B, aspectList);
    console.log(url);
    this.httpRequestService.register(url).subscribe(data => {
      console.log(data)
      this.reset();
      this.showLoading = false;
    })
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
