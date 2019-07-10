import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KeywordSearchComponent } from './keyword-search.component';

describe('KeywordSearchComponent', () => {
  let component: KeywordSearchComponent;
  let fixture: ComponentFixture<KeywordSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KeywordSearchComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KeywordSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
