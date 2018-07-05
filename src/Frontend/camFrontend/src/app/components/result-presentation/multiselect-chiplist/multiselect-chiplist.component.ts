import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatChipInputEvent } from '@angular/material';

@Component({
  selector: 'app-multiselect-chiplist',
  templateUrl: './multiselect-chiplist.component.html',
  styleUrls: ['./multiselect-chiplist.component.css']
})
export class MultiselectChiplistComponent {


  @Input() extractedAspects = new Array<string>();
  @Output() updatedSelection = new EventEmitter<Array<string>>();


  selectedAspects: any[] = [];


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

}
