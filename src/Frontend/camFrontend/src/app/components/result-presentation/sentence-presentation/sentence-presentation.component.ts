import { Component, OnInit, Input } from '@angular/core';
import { DispensableResult } from '../../../model/dispensable-result';
import { Aspect } from '../../../model/aspect';
import { Sentence } from '../../../model/sentence';
import { MatDialog } from '@angular/material';
import { ContextPresentationComponent } from '../../shared-components/context-presentation/context-presentation.component';

@Component({
  selector: 'app-sentence-presentation',
  templateUrl: './sentence-presentation.component.html',
  styleUrls: ['./sentence-presentation.component.css']
})
export class SentencePresentationComponent implements OnInit {

  @Input() dispensableResult: DispensableResult;
  @Input() isWinner: boolean;
  @Input() selectedAspects = new Array<string>();
  @Input() selectedEnteredAspects = new Array<string>();
  @Input() trigger = 0;
  @Input() finalAspectList = new Array<Aspect>();

  public sentences: Array<Sentence>;

  constructor(public dialog: MatDialog) { }

  ngOnInit() {
    /* @changes, Author: Ali
    */
   
    if (this.isWinner) {
      this.sentences = this.dispensableResult.obj1Sentences;
    } else {
      this.sentences = this.dispensableResult.obj2Sentences;
    }
  }

  getContext(id_pair) {
    const dialogRef = this.dialog.open(ContextPresentationComponent, {
      width: '45%',
      data: {
        dispensableResult: this.dispensableResult,
        finalAspectList: this.finalAspectList,
        selectedAspects: this.selectedAspects,
        IDpairs: id_pair
      }
    });
  }

  contextIsThere(sentence: Sentence) {
    return !('' in sentence.id_pair);
  }

  getKeyCount(dict: {}) {
    return Object.keys(dict).length;
  }

}
