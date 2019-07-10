import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultPresentationComponent } from './result-presentation.component';

describe('ResultPresentationComponent', () => {
  let component: ResultPresentationComponent;
  let fixture: ComponentFixture<ResultPresentationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ResultPresentationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResultPresentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
