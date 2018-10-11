import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Sentence } from '../../../model/sentence';
import { HTTPRequestService } from '../../../services/http-request.service';
import { UrlBuilderService } from '../../../services/url-builder.service';

@Component({
  selector: 'app-context-presentation',
  templateUrl: './context-presentation.component.html',
  styleUrls: ['./context-presentation.component.css']
})
export class ContextPresentationComponent {

  public showLoading = true;
  public sentences: Sentence[];
  public selectedRange: number;
  public documentIDs = new Array<string>();
  public selectedDocumentID: string;

  constructor(private httpService: HTTPRequestService, private urlService: UrlBuilderService,
    public dialogRef: MatDialogRef<ContextPresentationComponent>, @Inject(MAT_DIALOG_DATA) public data: any) {
      this.documentIDs = Object.keys(this.data.IDpairs);
      this.selectedDocumentID = this.documentIDs[0];
      this.getContext(3);
  }

  getContext(contextRange: number) {
    this.showLoading = true;
    this.selectedRange = contextRange;
    let url = '';
    if (contextRange !== -1) {
      url = this.urlService.getContextURL(this.selectedDocumentID, this.data.IDpairs[this.selectedDocumentID], contextRange);
    } else {
      url = this.urlService.getWholeContextURL(this.selectedDocumentID);
    }
    this.httpService.getContext(url).subscribe(
      result => {
        this.sentences = result;
        this.showLoading = false;
      },
      error => {
        console.error(error);
      }
    );
  }

  getValues(dict: {}) {
    return Object.values(dict);
  }

  documentIDChanged(contextRange: number) {
    this.getContext(contextRange);
  }

  documentIDSelected(documentID: string) {
    this.selectedDocumentID = documentID;
    this.getContext(3);
  }

  openLink() {
    window.open(this.selectedDocumentID, '_blank');
  }
}
