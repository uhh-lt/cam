import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SentencePresentationComponent } from './sentence-presentation.component';

describe('SentencePresentationComponent', () => {
  let component: SentencePresentationComponent;
  let fixture: ComponentFixture<SentencePresentationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SentencePresentationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SentencePresentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
