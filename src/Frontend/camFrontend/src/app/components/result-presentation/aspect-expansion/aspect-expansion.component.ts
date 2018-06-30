import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-aspect-expansion',
  templateUrl: './aspect-expansion.component.html',
  styleUrls: ['./aspect-expansion.component.css']
})
export class AspectExpansionComponent implements OnInit {

  private _aspectSentences = Array<string>();
  @Input() set aspectSentences(aspectSentences: Array<string>) {
    if (aspectSentences !== undefined) {
      this._aspectSentences = aspectSentences;
    }
  }
  @Input() titel: String;
  @Input() dispensableResult: any;
  @Input() finalAspectDict: any;
  @Input() summary: string;

  initialized = false;
  constructor() { }

  ngOnInit() {
    this.initialized = true;
  }


}
