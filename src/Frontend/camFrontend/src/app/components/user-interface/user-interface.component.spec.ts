import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UserInterfaceComponent } from './user-interface.component';

describe('UserInterfaceComponent', () => {
  let component: UserInterfaceComponent;
  let fixture: ComponentFixture<UserInterfaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UserInterfaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserInterfaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
