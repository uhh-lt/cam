import { Component, OnInit, Input } from '@angular/core';
import { DispensableResult } from '../../../model/dispensable-result';
import { Aspect } from '../../../model/aspect';
import { Sentence } from '../../../model/sentence';

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

  constructor() { }

  ngOnInit() {
    if (this.isWinner) {
      this.sentences = this.dispensableResult.winnerSentences;
    } else {
      this.sentences = this.dispensableResult.looserSentences;
    }


  }

}
