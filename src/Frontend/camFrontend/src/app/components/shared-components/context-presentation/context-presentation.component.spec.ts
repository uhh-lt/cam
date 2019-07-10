import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContextPresentationComponent } from './context-presentation.component';

describe('ContextPresentationComponent', () => {
  let component: ContextPresentationComponent;
  let fixture: ComponentFixture<ContextPresentationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContextPresentationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContextPresentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
