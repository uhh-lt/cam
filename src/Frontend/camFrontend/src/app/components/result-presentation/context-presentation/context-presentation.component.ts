import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
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
  public selectedRange: number;

  constructor(private httpService: HTTPRequestService, private urlService: UrlBuilderService,
    public dialogRef: MatDialogRef<ContextPresentationComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
      this.getContext(3);
  }

  getContext(contextRange: number) {
    this.showLoading = true;
    this.selectedRange = contextRange;
    let url = '';
    if (contextRange !== -1) {
      url = this.urlService.getContextURL(this.data.documentID, this.data.sentenceID, contextRange);
    } else {
      url = this.urlService.getWholeContextURL(this.data.documentID);
    }
    this.httpService.getContext(url).subscribe(
      result => {
        this.sentences = result;
        this.showLoading = false;
      }
    );
  }
}
