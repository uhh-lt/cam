import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MultiselectChiplistComponent } from './multiselect-chiplist.component';

describe('MultiselectChiplistComponent', () => {
  let component: MultiselectChiplistComponent;
  let fixture: ComponentFixture<MultiselectChiplistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MultiselectChiplistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MultiselectChiplistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
