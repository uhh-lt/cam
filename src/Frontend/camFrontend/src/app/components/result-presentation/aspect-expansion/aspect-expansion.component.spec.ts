import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AspectExpansionComponent } from './aspect-expansion.component';

describe('AspectExpansionComponent', () => {
  let component: AspectExpansionComponent;
  let fixture: ComponentFixture<AspectExpansionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AspectExpansionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AspectExpansionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
