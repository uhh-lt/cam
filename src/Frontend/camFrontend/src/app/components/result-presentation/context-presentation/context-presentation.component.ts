import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '../../../../../node_modules/@angular/material';
import { Sentence } from '../../../model/sentence';
import { HTTPRequestService } from '../../../shared/http-request.service';
import { UrlBuilderService } from '../../../shared/url-builder.service';

@Component({
  selector: 'app-context-presentation',
  templateUrl: './context-presentation.component.html',
  styleUrls: ['./context-presentation.component.css']
})
export class ContextPresentationComponent {

  public showLoading = true;
  public sentences: Sentence[];
  public contextRange = {
    Short: 2,
    Medium: 4,
    Document: 100
  };

  constructor(private httpService: HTTPRequestService, private urlService: UrlBuilderService,
    public dialogRef: MatDialogRef<ContextPresentationComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
      this.getContext(this.contextRange.Short);
  }

  getContext(contextRange: number) {
    this.httpService.getContext(this.urlService.getContextURL(this.data.documentID, this.data.sentenceID, contextRange)).subscribe(
      result => {
        this.sentences = result;
        this.showLoading = false;
      }
    );
  }

}
