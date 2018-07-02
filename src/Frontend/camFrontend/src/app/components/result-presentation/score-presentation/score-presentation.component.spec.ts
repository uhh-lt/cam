import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ScorePresentationComponent } from './score-presentation.component';

describe('ScorePresentationComponent', () => {
  let component: ScorePresentationComponent;
  let fixture: ComponentFixture<ScorePresentationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ScorePresentationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ScorePresentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
