import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '../../../../../node_modules/@angular/material';
import { Sentence } from '../../../model/sentence';

@Component({
  selector: 'app-context-presentation',
  templateUrl: './context-presentation.component.html',
  styleUrls: ['./context-presentation.component.css']
})
export class ContextPresentationComponent {

  public showLoading = true;
  public sentences: Sentence[];

  constructor(public dialogRef: MatDialogRef<ContextPresentationComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
    data.sentences.subscribe(
      result => {
        this.sentences = result;
        this.showLoading = false;
      }
    );



  }

}
