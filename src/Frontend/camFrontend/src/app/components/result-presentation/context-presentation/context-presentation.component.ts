import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '../../../../../node_modules/@angular/material';

@Component({
  selector: 'app-context-presentation',
  templateUrl: './context-presentation.component.html',
  styleUrls: ['./context-presentation.component.css']
})
export class ContextPresentationComponent {

  constructor(
    public dialogRef: MatDialogRef<ContextPresentationComponent>, @Inject(MAT_DIALOG_DATA) public data: any) { }

  onNoClick(): void {
    this.dialogRef.close();
  }


}
