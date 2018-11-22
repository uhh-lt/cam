import { Component, Input, Output, EventEmitter, ElementRef } from '@angular/core';
import { MatChipInputEvent } from '@angular/material';

@Component({
  selector: 'app-multiselect-chiplist',
  templateUrl: './multiselect-chiplist.component.html',
  styleUrls: ['./multiselect-chiplist.component.css']
})
export class MultiselectChiplistComponent {


  @Input() extractedAspects = new Array<string>();
  @Input() set arrange(position: string) {
    this.elementRef.nativeElement.style.setProperty('--align', position);
  }
  @Input() title = '';
  @Output() updatedSelection = new EventEmitter<Array<string>>();
  @Output() updatedMarks = new EventEmitter<Array<string>>();


  selectedAspects: any[] = [];
  markedAspects: any[] = [];

  constructor(private elementRef: ElementRef) { }

  isSelected(fruit: any): boolean {
    const index = this.selectedAspects.indexOf(fruit);
    return index >= 0;
  }


  selectAspect(fruit: any): void {
    const index = this.selectedAspects.indexOf(fruit);

    if (index >= 0) {
      this.selectedAspects.splice(index, 1);
    } else {
      this.selectedAspects.push(fruit);
    }

    this.updatedSelection.emit(this.selectedAspects);
  }

  isMarked(fruit: any): boolean {
    const index = this.markedAspects.indexOf(fruit);
    return index >= 0;
  }


  markAspect(fruit: any): void {
    const index = this.markedAspects.indexOf(fruit);

    if (index >= 0) {
      this.markedAspects.splice(index, 1);
    } else {
      this.markedAspects.push(fruit);
    }

    this.updatedMarks.emit(this.markedAspects);
  }

}
